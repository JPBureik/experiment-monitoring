# Experiment Monitoring Server Setup

## Hardware Requirements

  * Raspberry Pi 4B 8GB
  * Micro SD Card 128GB
  * 5V USB-C Power Supply
  * 2x 128GB USB key
  * Cooling Case for RPI

#### The instructions below are given for a Linux command line. Replace text in *italitcs*.

## Preparing the RaspberryPi

  * [Download](https://www.raspberrypi.org/downloads/raspbian/) and install Raspbian Buster Lite

  * Add an SSH file to the boot SD card:
    <code>
    touch boot/ssh
    </code>
  * Get IP address:
    <code>
    ping raspberrypi.local
    </code>
  * On your machine add ECDSA host key for RaspberryPi:
    <code>
    ssh-keygen -f “/home/<i>user</i>/.ssh/known_hosts” -R “<i>IP</i>”p
    </code>
  * SSH into RPI with default password `raspberry`:
    <code>
    ssh pi@IP
    </code>
  * Set root password:
    <code>
    sudo passwd root
    </code>
  * Enable root login via ssh:
    <code>
    sudo nano /etc/ssh/sshd_config -> set PermitRootLogin yes
    </code>
  * Reboot RPI:
    <code>
    sudo reboot
    </code>
  * SSH into RPI with new password:
    <code>
    ssh root@IP
    </code>
  * Create your user account (e.g. `admin`) and home directory:
    <code>
    usermod -l <i>newuser</i> pi
    usermod -m -d /home/newuser newuser
    </code>
  * logout
  * ssh newuser@IP (default password: raspberry)
  * passwd
  * Set new password for newuser account
  * Verify new user has sudo privileges: sudo apt-get update
  * Disable root: sudo passwd -l root
