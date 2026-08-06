#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "openai>=1.0",
#     "openai-agents>=0.2.0",
#     "rich>=13.0",
# ]
# ///
"""Workspace agent via OpenAI Agents SDK (shell restricted to the codespace)."""
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

# Block shell from reading host gate / secrets outside the codespace.
_BLOCKED_PATH_MARKERS = (
    "/opt/isc_gate",
    "completion_gate",
    "/proc/",
    "/etc/",
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
    """Return an error string if the command is not allowed."""
    lowered = command.lower()
    for marker in _BLOCKED_PATH_MARKERS:
        if marker.lower() in lowered:
            return f"Error: access denied ({marker})"
    # Disallow absolute paths outside workspace.
    for token in shlex.split(command, posix=True):
        if token.startswith("/") and not token.startswith(str(workspace)):
            # Allow common bins
            if token in {"/usr/bin/python3", "/usr/bin/python", "/bin/ls", "/bin/cat", "/bin/echo"}:
                continue
            if token.startswith(("/usr/bin/", "/bin/", "/usr/local/bin/")):
                continue
            return "Error: absolute paths outside the workspace are not allowed"
        if token.startswith(".."):
            return "Error: path traversal is not allowed"
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
            env={
                **os.environ,
                # Keep keys for task.py child processes; strip from accidental prints in parent.
            },
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
        "You are an autonomous agent. "
        "You have a shell tool to run any command in your workspace.\n\n"
        f"Your workspace is: {workspace}\n\n"
        "Complete the workflow so that the checks pass. "
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
            "You are an autonomous coding agent with one tool: shell. "
            "Stay inside the workspace. Use shell for ls, cat, python3, and edits.\n"
            "Packages openai and pydantic are installed.\n"
            "Complete the workflow so checks pass. Do not ask questions."
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
