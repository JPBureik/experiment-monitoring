#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Secure credentials management for experiment monitoring.

Credentials are loaded from environment variables first, then from a local
config file at ~/.expmonitor/credentials.json (which should never be committed
to version control).

Environment variables:
    EXPMONITOR_SSH_HOST: SSH server hostname or IP
    EXPMONITOR_SSH_PORT: SSH server port (default: 22)
    EXPMONITOR_SSH_USER: SSH username
    EXPMONITOR_SSH_PASSWORD: SSH password

Config file format (~/.expmonitor/credentials.json):
    {
        "ssh": {
            "host": "10.117.53.37",
            "port": 22,
            "user": "admin",
            "password": "your_password_here"
        }
    }
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, TypedDict


class SSHCredentials(TypedDict):
    """Type definition for SSH credentials."""

    host: str
    port: int
    user: str
    password: str


class CredentialsError(Exception):
    """Raised when required credentials are missing."""

    pass


class Credentials:
    """Manages secure credential storage and retrieval."""

    CONFIG_DIR: Path = Path.home() / ".expmonitor"
    CONFIG_FILE: Path = CONFIG_DIR / "credentials.json"

    @classmethod
    def _load_config_file(cls) -> dict[str, Any]:
        """Load credentials from JSON config file."""
        if not cls.CONFIG_FILE.exists():
            return {}
        with open(cls.CONFIG_FILE, "r") as f:
            result: dict[str, Any] = json.load(f)
            return result

    @classmethod
    def get_ssh_credentials(cls) -> SSHCredentials:
        """
        Get SSH credentials from environment or config file.

        Returns:
            SSHCredentials: Contains 'host', 'port', 'user', 'password' keys.

        Raises:
            CredentialsError: If required credentials are missing.
        """
        # Try environment variables first
        env_host = os.environ.get("EXPMONITOR_SSH_HOST")
        env_port = os.environ.get("EXPMONITOR_SSH_PORT", "22")
        env_user = os.environ.get("EXPMONITOR_SSH_USER")
        env_password = os.environ.get("EXPMONITOR_SSH_PASSWORD")

        if all([env_host, env_user, env_password]):
            return SSHCredentials(
                host=env_host,  # type: ignore[typeddict-item]
                port=int(env_port),
                user=env_user,  # type: ignore[typeddict-item]
                password=env_password,  # type: ignore[typeddict-item]
            )

        # Fall back to config file
        config = cls._load_config_file()
        ssh_config: dict[str, Any] = config.get("ssh", {})

        host = ssh_config.get("host")
        port = int(ssh_config.get("port", 22))
        user = ssh_config.get("user")
        password = ssh_config.get("password")

        missing = [
            k
            for k, v in [("host", host), ("user", user), ("password", password)]
            if not v
        ]
        if missing:
            raise CredentialsError(
                f"Missing SSH credentials: {', '.join(missing)}. "
                f"Set EXPMONITOR_SSH_* environment variables or create "
                f"{cls.CONFIG_FILE} with the required fields."
            )

        # At this point we know host, user, password are not None
        return SSHCredentials(
            host=str(host),
            port=port,
            user=str(user),
            password=str(password),
        )

    @classmethod
    def create_template_config(cls) -> None:
        """Create a template config file if none exists."""
        if cls.CONFIG_FILE.exists():
            print(f"Config file already exists: {cls.CONFIG_FILE}")
            return

        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        template = {
            "ssh": {
                "host": "YOUR_HOST_HERE",
                "port": 22,
                "user": "YOUR_USER_HERE",
                "password": "YOUR_PASSWORD_HERE",
            }
        }

        with open(cls.CONFIG_FILE, "w") as f:
            json.dump(template, f, indent=4)

        # Set restrictive permissions (owner read/write only)
        cls.CONFIG_FILE.chmod(0o600)

        print(f"Created template config: {cls.CONFIG_FILE}")
        print("Please edit this file with your actual credentials.")
