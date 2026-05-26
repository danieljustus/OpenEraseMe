import warnings

from symeraseme.cli import app

warnings.warn(
    "The 'openeraseme' CLI is deprecated. Use 'symeraseme' instead.",
    DeprecationWarning,
    stacklevel=2,
)

if __name__ == "__main__":
    app()
