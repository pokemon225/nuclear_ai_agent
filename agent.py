"""Minimal tool-using agent scaffold."""

from __future__ import annotations

import argparse
import shlex
from typing import Callable

Tool = Callable[[str], str]

TOOLS: dict[str, Tool] = {}


def tool(name: str) -> Callable[[Tool], Tool]:
    """Register a function as a named tool."""

    def register(fn: Tool) -> Tool:
        TOOLS[name] = fn
        return fn

    return register


@tool("echo")
def _echo(arg: str) -> str:
    return arg


@tool("upper")
def _upper(arg: str) -> str:
    return arg.upper()


@tool("wc")
def _wc(arg: str) -> str:
    return str(len(arg.split()))


def dispatch(line: str) -> str:
    """Run one `<tool> [args...]` command and return its output."""
    parts = shlex.split(line)
    if not parts:
        return ""
    name, arg = parts[0], " ".join(parts[1:])
    if name not in TOOLS:
        raise KeyError(f"unknown tool: {name} (available: {', '.join(sorted(TOOLS))})")
    return TOOLS[name](arg)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Minimal tool-using agent.")
    parser.add_argument("command", nargs="*", help="tool name followed by its arguments")
    parser.add_argument("--list", action="store_true", help="list available tools")
    args = parser.parse_args(argv)

    if args.list:
        for name in sorted(TOOLS):
            print(name)
        return 0

    if not args.command:
        parser.print_help()
        return 1

    try:
        print(dispatch(" ".join(args.command)))
    except KeyError as exc:
        print(exc.args[0])
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
