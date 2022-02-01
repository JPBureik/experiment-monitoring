#!/usr/bin/bash

echo "Installing ..."
timedatectl set-timezone Europe/Paris
apt update && sudo apt -y upgrade
apt install xorg
echo "Done."