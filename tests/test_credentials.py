#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for credentials module."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from expmonitor.utilities.credentials import Credentials, CredentialsError


class TestCredentials:
    """Tests for Credentials class."""

    def test_get_ssh_credentials_from_env(self) -> None:
        """Test reading SSH credentials from environment variables."""
        env = {
            "EXPMONITOR_SSH_HOST": "example.com",
            "EXPMONITOR_SSH_PORT": "2222",
            "EXPMONITOR_SSH_USER": "testuser",
            "EXPMONITOR_SSH_PASSWORD": "testpass",
        }
        with patch.dict(os.environ, env, clear=False):
            creds = Credentials.get_ssh_credentials()
            assert creds["host"] == "example.com"
            assert creds["port"] == 2222
            assert creds["user"] == "testuser"
            assert creds["password"] == "testpass"

    def test_get_ssh_credentials_from_config_file(self) -> None:
        """Test reading SSH credentials from config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir)
            config_file = config_dir / "credentials.json"
            config_file.write_text(
                json.dumps(
                    {
                        "ssh": {
                            "host": "filehost.com",
                            "port": 22,
                            "user": "fileuser",
                            "password": "filepass",
                        }
                    }
                )
            )

            # Clear env vars and patch config path
            env_clear = {
                "EXPMONITOR_SSH_HOST": "",
                "EXPMONITOR_SSH_USER": "",
                "EXPMONITOR_SSH_PASSWORD": "",
            }
            with patch.dict(os.environ, env_clear, clear=False):
                with patch.object(Credentials, "CONFIG_FILE", config_file):
                    creds = Credentials.get_ssh_credentials()
                    assert creds["host"] == "filehost.com"
                    assert creds["port"] == 22
                    assert creds["user"] == "fileuser"
                    assert creds["password"] == "filepass"

    def test_get_ssh_credentials_missing_raises_error(self) -> None:
        """Test that missing credentials raise CredentialsError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "credentials.json"
            # Empty config
            config_file.write_text(json.dumps({}))

            env_clear = {
                "EXPMONITOR_SSH_HOST": "",
                "EXPMONITOR_SSH_USER": "",
                "EXPMONITOR_SSH_PASSWORD": "",
            }
            with patch.dict(os.environ, env_clear, clear=False):
                with patch.object(Credentials, "CONFIG_FILE", config_file):
                    with pytest.raises(CredentialsError) as exc_info:
                        Credentials.get_ssh_credentials()
                    assert "Missing SSH credentials" in str(exc_info.value)

    def test_create_template_config(self) -> None:
        """Test template config file creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_dir = Path(tmpdir) / ".expmonitor"
            config_file = config_dir / "credentials.json"

            with patch.object(Credentials, "CONFIG_DIR", config_dir):
                with patch.object(Credentials, "CONFIG_FILE", config_file):
                    Credentials.create_template_config()

                    assert config_file.exists()
                    content = json.loads(config_file.read_text())
                    assert "ssh" in content
                    assert "host" in content["ssh"]
                    assert "port" in content["ssh"]
                    assert "user" in content["ssh"]
                    assert "password" in content["ssh"]

    def test_env_takes_precedence_over_config(self) -> None:
        """Test that environment variables take precedence over config file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_file = Path(tmpdir) / "credentials.json"
            config_file.write_text(
                json.dumps(
                    {
                        "ssh": {
                            "host": "filehost.com",
                            "port": 22,
                            "user": "fileuser",
                            "password": "filepass",
                        }
                    }
                )
            )

            env = {
                "EXPMONITOR_SSH_HOST": "envhost.com",
                "EXPMONITOR_SSH_USER": "envuser",
                "EXPMONITOR_SSH_PASSWORD": "envpass",
            }
            with patch.dict(os.environ, env, clear=False):
                with patch.object(Credentials, "CONFIG_FILE", config_file):
                    creds = Credentials.get_ssh_credentials()
                    # Should use env values, not file values
                    assert creds["host"] == "envhost.com"
                    assert creds["user"] == "envuser"
