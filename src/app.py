"""app.py - interactive explainer.

Run from the repository root with:

    uv run marimo run src/app.py

Edit with:

    uv run marimo edit src/app.py
"""

import marimo

__generated_with = "0.19.7"
app = marimo.App(width="full")


@app.cell
def _():
    from pathlib import Path

    import marimo as mo

    from app_core import (
        filter_items,
        get_item_by_path,
        get_tree_label,
        index_items_by_path,
        load_project_data,
    )

    return (
        Path,
        filter_items,
        get_item_by_path,
        get_tree_label,
        index_items_by_path,
        load_project_data,
        mo,
    )


@app.cell
def _(index_items_by_path, load_project_data, mo):
    notebook_location = mo.notebook_location()
    if notebook_location is None:
        raise RuntimeError("Unable to determine notebook location.")

    data_path = notebook_location / "public" / "data.toml"

    project, items = load_project_data(data_path)
    items_by_path = index_items_by_path(items)

    return items, items_by_path, project


@app.cell
def _(mo):
    get_selected_path, set_selected_path = mo.state("README.md")
    return get_selected_path, set_selected_path


@app.cell
def _(mo):
    show_all = mo.ui.switch(
        value=False,
        label="Show all files",
    )
    return (show_all,)


@app.cell
def _(
    filter_items,
    get_tree_label,
    items,
    mo,
    project,
    set_selected_path,
    show_all,
):
    visible_items = filter_items(
        items,
        highlighted_only=not show_all.value,
    )

    def make_tree_button(item):
        path = str(item["path"])
        attention = bool(item["attention"])

        button = mo.ui.button(
            label=get_tree_label(item),
            kind="warn" if attention else "neutral",
            tooltip=str(item["description"]),
            on_click=lambda _value, selected=path: (
                set_selected_path(selected),
                selected,
            )[1],
        )

        return mo.hstack(
            [button],
            justify="start",
        )

    tree_rows = [make_tree_button(item) for item in visible_items]

    tree_panel = mo.vstack(
        [
            mo.md(
                rf"""
## {project["source_project"]}

**Highlighted entries hold key project-specific content.**
"""
            ),
            show_all,
            mo.vstack(tree_rows, gap=0.08).style(
                max_height="70vh",
                overflow="auto",
                padding="0.25rem",
            ),
        ],
        gap=0.5,
    )

    return (tree_panel,)


@app.cell
def _(get_item_by_path, get_selected_path, items_by_path, mo):
    selected_path = get_selected_path()
    selected = get_item_by_path(items_by_path, selected_path)

    details_panel = mo.md(
        rf"""
## `{selected["path"]}`

---

### Description

{selected["description"]}

---

### Rationale

{selected["rationale"]}

---

[**🔗 Example**](https://github.com/denisecase/datafun-01-foundations)
"""
    ).callout(kind="warn" if selected["attention"] else "neutral")

    return (details_panel,)


@app.cell
def _(details_panel, mo, project, tree_panel):
    mo.vstack(
        [
            mo.md(
                rf"""
# {project["title"]}

A Marimo app that explains common files and folders in a professional Python project.
Each entry is **clickable**; highlighted entries hold key project-specific content.
[🔗 View source](https://github.com/denisecase/professional-python-project-explainer).

---
"""
            ),
            mo.hstack(
                [tree_panel, details_panel],
                widths=[1.15, 1.0],
                align="start",
                wrap=True,
                gap=1.25,
            ),
        ],
        gap=1.0,
    )


if __name__ == "__main__":
    app.run()
