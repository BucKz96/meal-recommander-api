"""Tests for the CLI entrypoint defined in src.api.main."""

from types import SimpleNamespace
from unittest.mock import patch

from src.api import main as api_main


def test_main_invokes_uvicorn_run() -> None:
    """Ensure that calling main() démarre bien Uvicorn avec la config attendue."""

    dummy_settings = SimpleNamespace(
        api_host="127.0.0.1",
        api_port=9999,
        api_reload=False,
        log_level="INFO",
    )

    with (
        patch("src.api.main.get_settings", return_value=dummy_settings),
        patch("uvicorn.run") as mock_run,
    ):
        api_main.main()

    mock_run.assert_called_once_with(
        "src.api.main:app",
        host=dummy_settings.api_host,
        port=dummy_settings.api_port,
        reload=dummy_settings.api_reload,
        log_level=dummy_settings.log_level.lower(),
    )
