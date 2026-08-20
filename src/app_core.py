"""app_core.py - reusable logic."""

import tomllib
from pathlib import Path, PurePath
from typing import Any
from urllib.request import urlopen


def load_project_data(
    data_path: Path | PurePath | str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Load project metadata and project structure items from TOML."""
    location = str(data_path)

    if location.startswith(("http://", "https://")):
        with urlopen(location) as response:
            project_data = tomllib.loads(response.read().decode("utf-8"))
    else:
        with Path(location).open("rb") as file:
            project_data = tomllib.load(file)

    project = project_data["project"]
    items = project_data["item"]

    return project, items


def index_items_by_path(
    items: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Index project structure items by path."""
    return {str(item["path"]): item for item in items}


def get_item_by_path(
    items_by_path: dict[str, dict[str, Any]],
    path: str,
) -> dict[str, Any]:
    """Return the project structure item for a path."""
    return items_by_path[path]


def get_tree_label(item: dict[str, Any]) -> str:
    """Return the Markdown label for a project structure item."""
    line = str(item["line"])
    attention = bool(item["attention"])

    return f"**`{line}`**" if attention else f"`{line}`"
