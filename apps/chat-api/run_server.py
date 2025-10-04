"""Convenience launcher for the FastAPI app."""

import os
import sys

import uvicorn

from src.core.config import settings


def _ensure_project_on_path() -> None:
    """Guarantee the project root is importable when running as a script."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


if __name__ == "__main__":
    _ensure_project_on_path()
    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
    )

# Add the current directory to Python path
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# if __name__ == "__main__":
#     uvicorn.run(
#         "src.main:app",
#         host="127.0.0.1",
#         port=8000,
#         reload=True,
#         reload_dirs=["."]
#     )
