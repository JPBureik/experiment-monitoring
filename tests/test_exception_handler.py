#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for exception handler module."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

from expmonitor.utilities.exception_handler import ExceptionHandler


class TestExceptionHandler:
    """Tests for ExceptionHandler class."""

    def test_default_settings(self) -> None:
        """Test default configuration values."""
        handler = ExceptionHandler()
        assert handler.overwrite_log_file is True
        assert handler.log_full_tb is False
        assert handler.verbose is False

    def test_overwrite_log_file_setter(self) -> None:
        """Test overwrite_log_file property setter."""
        handler = ExceptionHandler()
        handler.overwrite_log_file = False
        assert handler.overwrite_log_file is False

    def test_overwrite_log_file_setter_ignores_non_bool(self) -> None:
        """Test that non-bool values are ignored."""
        handler = ExceptionHandler()
        handler.overwrite_log_file = "not a bool"  # type: ignore[assignment]
        assert handler.overwrite_log_file is True  # unchanged

    def test_log_full_tb_setter(self) -> None:
        """Test log_full_tb property setter."""
        handler = ExceptionHandler()
        handler.log_full_tb = True
        assert handler.log_full_tb is True

    def test_verbose_setter(self) -> None:
        """Test verbose property setter."""
        handler = ExceptionHandler()
        handler.verbose = True
        assert handler.verbose is True

    def test_create_log_file(self) -> None:
        """Test log file creation."""
        handler = ExceptionHandler()
        with tempfile.TemporaryDirectory() as tmpdir:
            handler.log_dir = Path(tmpdir)
            handler.create_log_file()
            assert handler.log_file.exists()
            assert handler.log_file.name.startswith("log_")
            assert handler.log_file.name.endswith(".txt")

    def test_create_log_file_creates_directory(self) -> None:
        """Test that create_log_file creates the log directory if needed."""
        handler = ExceptionHandler()
        with tempfile.TemporaryDirectory() as tmpdir:
            new_dir = Path(tmpdir) / "newdir"
            handler.log_dir = new_dir
            handler.create_log_file()
            assert new_dir.exists()
            assert handler.log_file.exists()

    def test_log_exception(self) -> None:
        """Test exception logging."""
        handler = ExceptionHandler()
        with tempfile.TemporaryDirectory() as tmpdir:
            handler.log_dir = Path(tmpdir)
            handler.create_log_file()

            # Create mock sensor
            mock_sensor = MagicMock()
            mock_sensor.descr = "test_sensor"

            # Log an exception
            test_exception = ValueError("test error message")
            handler.log_exception(mock_sensor, test_exception)

            # Verify log content
            log_content = handler.log_file.read_text()
            assert "test_sensor" in log_content
            assert "ValueError" in log_content
            assert "test error message" in log_content
