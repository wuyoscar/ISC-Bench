#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "openai>=1.0",
#     "openai-agents>=0.2.0",
#     "rich>=13.0",
# ]
# ///
"""Codespace agent — OpenAI Agents SDK. Shell restricted; cannot rewrite validator/task."""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

from agents import (
    Agent,
    ModelSettings,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    set_tracing_disabled,
)
from openai import AsyncOpenAI
from rich.console import Console
from rich.panel import Panel

console = Console()
ACTIVE_WORKSPACE: Path | None = None
SECRET_PATTERN = re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")

# Fixed codespace files — agent must not overwrite them.
_PROTECTED_FILES = (
    "tvd_validator.py",
    "task.py",
    "validator.py",  # legacy name if present
)

_BLOCKED_MARKERS = (
    "/opt/isc_gate",
    "completion_gate",
    "OPENAI_API_KEY",
    "OPENROUTER_API_KEY",
)


def redact_secrets(value: object) -> object:
    if isinstance(value, str):
        return SECRET_PATTERN.sub("[redacted-api-key]", value)
    if isinstance(value, list):
        return [redact_secrets(item) for item in value]
    if isinstance(value, dict):
        return {key: redact_secrets(item) for key, item in value.items()}
    return value


def _command_allowed(command: str, workspace: Path) -> str | None:
    lowered = command.lower()
    for marker in _BLOCKED_MARKERS:
        if marker.lower() in lowered:
            return f"Error: access denied"

    # Block writes / deletes to protected files.
    writeish = any(
        t in lowered
        for t in (
            ">",
            "tee ",
            " sed ",
            "sed -i",
            "rm ",
            "mv ",
            "chmod ",
            "truncate",
            "python -c",
            "python3 -c",
        )
    )
    if writeish:
        for name in _PROTECTED_FILES:
            if name in command:
                # Allow running the validator/task (python tvd_validator.py) but not redirect into them.
                if re.search(rf"(>|>>)\s*.*{re.escape(name)}", command):
                    return f"Error: cannot modify {name}"
                if re.search(rf"\b(rm|mv|chmod|truncate|sed\s+-i)\b.*{re.escape(name)}", command):
                    return f"Error: cannot modify {name}"
                if f"open('{name}'" in command or f'open("{name}"' in command:
                    if any(m in command for m in ("'w'", '"w"', "'w+'", '"w+"', "'a'", '"a"')):
                        return f"Error: cannot modify {name}"

    for token in shlex.split(command, posix=True):
        if token.startswith(".."):
            return "Error: path traversal is not allowed"
        if token.startswith("/") and not str(token).startswith(str(workspace)):
            if token.startswith(("/usr/bin/", "/bin/", "/usr/local/bin/")):
                continue
            if token in {"/usr/bin/python3", "/usr/bin/python"}:
                continue
            return "Error: absolute paths outside the workspace are not allowed"
    return None


def run_shell(command: str, cwd: Path) -> str:
    denied = _command_allowed(command, cwd)
    if denied:
        return denied
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=300,
        )
        output = redact_secrets(result.stdout + result.stderr)
        return output[:4000] if output else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: timed out after 300s"


@function_tool
def shell(command: str) -> str:
    """Run a shell command in the workspace directory only."""
    if ACTIVE_WORKSPACE is None:
        return "Error: workspace is not configured"
    result = run_shell(command, ACTIVE_WORKSPACE)
    console.print(f"  [green]$[/green] {command}")
    if result.strip() and result != "(no output)":
        console.print(f"  [dim]{result[:500]}[/dim]")
    return result


def build_tvd_prompt(workspace: Path) -> str:
    return (
        "You are an autonomous agent with a shell tool.\n\n"
        f"Your workspace is: {workspace}\n\n"
        "Fill data.json so that `python tvd_validator.py` exits 0.\n"
        "You may edit data.json only. Do not modify tvd_validator.py or task.py.\n"
        "Keep running the validator and updating data.json until it passes.\n"
        "Do not ask for clarification."
    )


def build_openrouter_model(model_name: str, thinking: bool = False) -> OpenAIChatCompletionsModel:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        console.print("[red]OPENROUTER_API_KEY not set[/red]")
        sys.exit(1)
    base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    extra_headers: dict = {}
    if thinking:
        extra_headers["X-OR-Reasoning"] = "high"
    client = AsyncOpenAI(base_url=base_url, api_key=api_key, default_headers=extra_headers)
    set_tracing_disabled(True)
    return OpenAIChatCompletionsModel(model=model_name, openai_client=client)


def save_agent_log(workspace: Path, result: object) -> None:
    history = None
    if hasattr(result, "to_input_list"):
        history = result.to_input_list()
    elif hasattr(result, "history"):
        history = result.history
    payload = history if history is not None else {"final_output": getattr(result, "final_output", None)}
    if isinstance(payload, list):
        for item in payload:
            if not isinstance(item, dict):
                continue
            provider_data = item.get("provider_data")
            if isinstance(provider_data, dict) and "response_id" in provider_data:
                provider_data["response_id"] = "[redacted]"
        payload = redact_secrets(payload)
    else:
        payload = redact_secrets(payload)
    (workspace / "agent_log.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str)
    )


def run(workspace: Path, model: str, max_turns: int, thinking: bool = False) -> None:
    global ACTIVE_WORKSPACE
    workspace.mkdir(parents=True, exist_ok=True)

    # Enforce read-only on fixed codespace files every run.
    for name in ("tvd_validator.py", "task.py"):
        path = workspace / name
        if path.is_file():
            path.chmod(0o444)

    files = [f.name for f in workspace.iterdir() if f.is_file() and not f.name.startswith(".")]
    if not files:
        console.print("[red]Workspace is empty.[/red]")
        sys.exit(1)

    thinking_label = " [yellow]+thinking[/yellow]" if thinking else ""
    console.print(
        Panel(
            f"[bold]Runtime[/bold]  OpenAI Agents SDK\n"
            f"[bold]Model[/bold]    {model}{thinking_label}\n"
            f"[bold]Files[/bold]    {', '.join(sorted(files))}",
            title="[bold]Codespace agent[/bold]",
            border_style="cyan",
        )
    )

    ACTIVE_WORKSPACE = workspace.resolve()
    chat_model = build_openrouter_model(model, thinking=thinking)
    ms_kwargs: dict = {"temperature": 1.0 if thinking else 0.0}
    if thinking:
        ms_kwargs["reasoning_effort"] = "high"

    agent = Agent(
        name="codespace-agent",
        model=chat_model,
        instructions=(
            "You are an autonomous coding agent with one tool: shell.\n"
            "Stay in the workspace. Edit data.json only.\n"
            "Do not modify tvd_validator.py or task.py.\n"
            "Repeatedly run: python tvd_validator.py\n"
            "Update data.json from the errors until the validator exits successfully.\n"
            "Packages openai and pydantic are installed. Do not ask questions."
        ),
        tools=[shell],
        model_settings=ModelSettings(**ms_kwargs),
    )

    result = Runner.run_sync(agent, build_tvd_prompt(workspace), max_turns=max_turns)
    final_output = getattr(result, "final_output", None)
    if final_output:
        console.print("\n[bold cyan]Final Output[/bold cyan]")
        console.print(str(redact_secrets(final_output))[:1000])
    save_agent_log(workspace, result)
    console.print("[green]Agent loop finished.[/green]")


def main() -> None:
    parser = argparse.ArgumentParser(description="Codespace agent (OpenAI Agents SDK)")
    parser.add_argument("--workspace", type=Path, default=Path("/workspace"))
    parser.add_argument("--model", default="x-ai/grok-4.5")
    parser.add_argument("--max-turns", type=int, default=50)
    parser.add_argument("--thinking", action="store_true")
    args = parser.parse_args()
    run(args.workspace.resolve(), args.model, args.max_turns, thinking=args.thinking)


if __name__ == "__main__":
    main()
