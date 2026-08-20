# Professional Python Project Explainer

A small standalone Marimo app for helping new Python users understand the files and folders in a professional Python project.

The first version uses the `datafun-01-foundations` project shape supplied manually in `data.toml`.

Highlighted entries are the places students should pay attention to first. Every entry is clickable and explains what it is, why it exists, and what a student should do with it.

## Run

```powershell
uv sync
uv run marimo run src/app.py
```

## Edit

```powershell
uv run marimo edit app.py
```

## Maintain

- `data.toml` owns the ordered tree and explanatory metadata.
- `app.py` only renders the data.
- Later, an automated workflow can regenerate the tree entries from a canonical project while preserving or validating the explanatory metadata by `path`.
