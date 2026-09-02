# Nuclear AI Agent

A minimal, dependency-free scaffold for a tool-using agent.

## Usage

```bash
python3 agent.py --list            # show registered tools
python3 agent.py upper "hello"     # -> HELLO
python3 agent.py wc one two three  # -> 3
```

## Adding a tool

Tools are plain functions taking a string and returning a string. Register one
with the `@tool` decorator and it becomes available to the CLI immediately:

```python
@tool("reverse")
def _reverse(arg: str) -> str:
    return arg[::-1]
```

## Tests

```bash
pytest
```
