"""Tests for app_core.py reusable logic."""

from io import BytesIO
from pathlib import Path
from typing import Any

import pytest

import app_core
from app_core import (
    filter_items,
    get_item_by_path,
    get_tree_label,
    index_items_by_path,
    load_project_data,
)


def make_items() -> list[dict[str, Any]]:
    """Create representative project structure items."""
    return [
        {
            "path": "README.md",
            "line": "├── README.md",
            "attention": True,
        },
        {
            "path": "uv.lock",
            "line": "└── uv.lock",
            "attention": False,
        },
    ]


def test_filter_items_returns_all_items() -> None:
    """Verify filtering can retain all items."""
    items = make_items()

    result = filter_items(items, highlighted_only=False)

    assert result == items


def test_filter_items_returns_highlighted_only() -> None:
    """Verify filtering retains only highlighted items."""
    items = make_items()

    result = filter_items(items, highlighted_only=True)

    assert len(result) == 1
    assert result[0]["path"] == "README.md"


def test_get_tree_label_highlighted() -> None:
    """Verify highlighted labels use bold Markdown."""
    item = make_items()[0]

    assert get_tree_label(item) == "**`├── README.md`**"


def test_get_tree_label_normal() -> None:
    """Verify normal labels use plain Markdown code formatting."""
    item = make_items()[1]

    assert get_tree_label(item) == "`└── uv.lock`"


def test_index_items_by_path() -> None:
    """Verify items are indexed using their paths."""
    items = make_items()

    indexed = index_items_by_path(items)

    assert indexed["README.md"] == items[0]
    assert indexed["uv.lock"] == items[1]


def test_get_item_by_path() -> None:
    """Verify an indexed item can be retrieved by path."""
    items = make_items()
    indexed = index_items_by_path(items)

    result = get_item_by_path(indexed, "README.md")

    assert result["attention"] is True


def test_get_item_by_path_missing() -> None:
    """Verify an unknown path raises KeyError."""
    indexed = index_items_by_path(make_items())

    with pytest.raises(KeyError):
        get_item_by_path(indexed, "missing.py")


def test_load_project_data_from_file(tmp_path: Path) -> None:
    """Verify project metadata and items load from a local TOML file."""
    data_path = tmp_path / "data.toml"
    data_path.write_text(
        """
[project]
title = "Example Project"

[[item]]
path = "README.md"
line = "README.md"
attention = true
description = "Project overview."
rationale = "Introduces the project."
""",
        encoding="utf-8",
    )

    project, items = load_project_data(data_path)

    assert project["title"] == "Example Project"
    assert len(items) == 1
    assert items[0]["path"] == "README.md"
    assert items[0]["attention"] is True


def test_load_project_data_from_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Verify remote TOML loading without making a network request."""
    content = b"""
[project]
title = "Remote Project"

[[item]]
path = "src/app.py"
attention = true
"""

    def fake_urlopen(url: str) -> BytesIO:
        """Return simulated HTTP response content."""
        assert url == "https://example.org/data.toml"
        return BytesIO(content)

    monkeypatch.setattr(app_core, "urlopen", fake_urlopen)

    project, items = load_project_data("https://example.org/data.toml")

    assert project["title"] == "Remote Project"
    assert len(items) == 1
    assert items[0]["path"] == "src/app.py"
