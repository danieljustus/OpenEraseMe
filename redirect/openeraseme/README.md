# openeraseme — Deprecated Redirect Package

> **This package has been renamed to `symeraseme`.**
>
> Please update your dependencies:
>
> ```bash
> pip install symeraseme
> ```

`openeraseme` is a deprecated redirect package that exists only to help users
transition to the new name. It installs `symeraseme` as a dependency and
re-exports its entire API, while emitting a `DeprecationWarning` on import.

## Migration

Replace `openeraseme` with `symeraseme` in your `requirements.txt`,
`pyproject.toml`, or installation command:

```bash
# Old (deprecated)
pip install openeraseme

# New
pip install symeraseme
```

## Links

- New package: https://pypi.org/project/symeraseme/
- Repository: https://github.com/danieljustus/symaira-eraseme
