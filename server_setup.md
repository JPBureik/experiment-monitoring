# Experiment Monitoring Server Setup

## Recommended Hardware

  * Raspberry Pi 4B 8GB
  * Micro SD Card 128GB
  * 5V USB-C Power Supply
  * 2x 128GB USB thumb drive
  * Cooling Case for RPI

#### The instructions below are given for a Linux command line. Replace text in *italitcs*.

## Preparing the RaspberryPi

  * [Download](https://www.raspberrypi.org/downloads/raspbian/) and install Raspbian Buster Lite

  * Add an SSH file to the boot SD card:<br>
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
    ssh pi@<i>IP</i>
    </code>
  * Set root password:
    <code>
    sudo passwd root
    </code>
  * Enable root login via ssh:
    <code>
    sudo nano /etc/ssh/sshd_config
      &emsp; PermitRootLogin yes
    </code>
  * Reboot RPI:
    <code>
    sudo reboot
    </code>
  * SSH into RPI with new password:
    <code>
    ssh root@<i>IP</i>
    </code>
  * Create your user account (e.g. <code><i>admin</i></code>) and home directory:
    <code>
    usermod -l <i>admin</i> pi
    usermod -m -d /home/<i>admin</i> <i>admin</i>
    </code>
  * Log back in as new user with default password `raspberry`:
    <code>
    logout
    ssh <i>admin</i>@<i>IP</i>
    </code>
  * Set new password for <code><i>admin</i></code> account:
    <code>
    passwd
    </code>
  * Verify new user has sudo privileges:
    <code>
    sudo apt-get update
    </code>
  * Disable root:
    <code>
    sudo passwd -l root
    </code>

## Configuring the RPI
  * Enter configuration menu:
    <code>
    sudo raspi-config
    </code>

  * Network options:
    <code>
    hostname
      &emsp; <i>myserver</i>
    </code>
  * Reboot:
    <code>
    sudo reboot
    </code>
  * Log in with new hostname:
    <code>
    ssh <i>admin</i>@<i>myserver</i>.local
    </code>
  * Make sure everything is up-to-date:
    <code>
    sudo apt update && sudo apt -y upgrade
    </code>
  * Reboot:
    <code>
    sudo reboot
    </code>

## Adding external storage devices
  * Plug in both USB thumb drives and verify that they are recognized as `/dev/sda` and `/dev/sdb`:
    <code>
    lsblk
    </code>

  * Install the RAID software manager:
    <code>
    sudo apt-get install mdadm
    </code>
  * Create RAID1 array (e.g. <code><i>md0</i></code>):
  * <code>
    sudo mdadm --create --verbose /dev/<i>md0</i> --level=1 --raid-devices=2 /dev/sda /dev/sdb
    </code>
  * Check progress:
    <code>
    cat /proc/mdstat
    </code>
  * Create a filesystem on the RAID1 array:
    <code>
    sudo mkfs.ext4 -F /dev/md0
    </code>
