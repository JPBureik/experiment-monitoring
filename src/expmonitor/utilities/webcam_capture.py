#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 15:10:48 2022

@author: jp

Webcam capture utility for experiment monitoring.

Captures images from a webcam and transfers them to a remote server via SCP.
"""

from __future__ import annotations

import os
import time
from typing import Any

import cv2
import paramiko  # type: ignore[import-untyped]
from scp import SCPClient  # type: ignore[import-untyped]

from expmonitor.utilities.credentials import Credentials, CredentialsError


def create_ssh_client(
    host: str, port: int, user: str, password: str
) -> paramiko.SSHClient:
    """Create and return an SSH client connection."""
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, user, password)
    return client


def setup(savepath: str, remote_path: str) -> tuple[str, Any, SCPClient, str]:
    """
    Initialize webcam and SSH connection.

    Args:
        savepath: Local path to save captured images.
        remote_path: Remote path to transfer images to.

    Returns:
        Tuple of (savepath, cam, scp).
    """
    cam = cv2.VideoCapture(0)

    creds = Credentials.get_ssh_credentials()
    ssh = create_ssh_client(
        creds["host"], creds["port"], creds["user"], creds["password"]
    )
    scp = SCPClient(ssh.get_transport())

    return savepath, cam, scp, remote_path


def iteration(savepath: str, cam: Any, scp: SCPClient, remote_path: str) -> None:
    """Capture a single image and transfer it."""
    result, image = cam.read()

    if result:
        print("Picture taken.")
        save_result = cv2.imwrite(savepath, image)
        if save_result:
            print("Picture saved.")
        scp.put(savepath, remote_path)
        print("Picture sent.")
        os.remove(savepath)


if __name__ == "__main__":
    # Example configuration - adjust paths as needed
    local_savepath = r"C:\Users\Lattice\Pictures\expmonitor\zeeman2\z2.png"
    remote_savepath = "/mnt/data/webcam/zeeman2"

    try:
        savepath, cam, scp, remote_path = setup(local_savepath, remote_savepath)
    except CredentialsError as e:
        print(f"Credentials error: {e}")
        print("\nTo create a template config file, run:")
        print("  from expmonitor.utilities.credentials import Credentials")
        print("  Credentials.create_template_config()")
        exit(1)

    while True:
        try:
            iteration(savepath, cam, scp, remote_path)
        except KeyboardInterrupt:
            print("\nStopping webcam capture.")
            break
        except Exception as e:
            print(f"Error during capture: {e}")
            continue
        time.sleep(5)
