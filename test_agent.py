import pytest

from agent import TOOLS, dispatch, main


def test_registry_populated():
    assert {"echo", "upper", "wc"} <= set(TOOLS)


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("echo hi there", "hi there"),
        ("upper hi", "HI"),
        ("wc one two three", "3"),
        ("", ""),
    ],
)
def test_dispatch(line, expected):
    assert dispatch(line) == expected


def test_dispatch_quotes_are_respected():
    assert dispatch('echo "a b"  c') == "a b c"


def test_unknown_tool_raises():
    with pytest.raises(KeyError, match="unknown tool: nope"):
        dispatch("nope x")


def test_main_lists_tools(capsys):
    assert main(["--list"]) == 0
    assert "upper" in capsys.readouterr().out


def test_main_reports_unknown_tool(capsys):
    assert main(["nope"]) == 1
    assert "unknown tool" in capsys.readouterr().out


def test_main_without_command_is_usage_error():
    assert main([]) == 1
