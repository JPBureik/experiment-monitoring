# Experiment Monitoring Server Setup

## Recommended Hardware

  * Raspberry Pi 4B 8GB
  * Micro SD Card 128GB
  * 5V USB-C Power Supply
  * 2x 128GB USB thumb drive
  * Cooling Case for RPI
  * PC with an SD card reader

#### The instructions below are given for a Linux command line. SSH will generally work from the command prompt on Windows 10 and newer. Replace text in *italitcs*.

## Preparing the RaspberryPi

  * [Download](https://www.raspberrypi.org/downloads/raspbian/) and install Raspbian Buster Lite on the SD card

  * Add an SSH file to the boot SD card:
    <pre>
    touch boot/ssh
    </pre>
  * Get IP address:
    <pre>
    ping raspberrypi.local
    </pre>
  * On your machine add ECDSA host key for RaspberryPi:
    <pre>
    ssh-keygen -f “/home/<i>user</i>/.ssh/known_hosts” -R “<i>IP</i>”p
    </pre>
  * SSH into RPI with default password `raspberry`:
    <pre>
    ssh pi@<i>IP</i>
    </pre>
  * Set root password:
    <pre>
    sudo passwd root
    </pre>
  * Enable root login via ssh:
    <pre>
    sudo nano /etc/ssh/sshd_config
      &emsp; PermitRootLogin yes
    </pre>
  * Reboot RPI:
    <pre>
    sudo reboot
    </pre>
  * SSH into RPI with new password:
    <pre>
    ssh root@<i>IP</i>
    </pre>
  * Create your user account (e.g. <code><i>admin</i></code>) and home directory:
    <pre>
    usermod -l <i>admin</i> pi
    usermod -m -d /home/<i>admin</i> <i>admin</i>
    </pre>
  * Log back in as new user with default password `raspberry`:
    <pre>
    logout
    ssh <i>admin</i>@<i>IP</i>
    </pre>
  * Set new password for <code><i>admin</i></code> account:
    <pre>
    passwd
    </pre>
  * Verify new user has sudo privileges:
    <pre>
    sudo apt-get update
    </pre>
  * Disable root:
    <pre>
    sudo passwd -l root
    </pre>

## Configuring the RPI
  * Enter configuration menu:
    <pre>
    sudo raspi-config
    </pre>

  * Network options:
    <pre>
    hostname
      &emsp; <i>myserver</i>
    </pre>
  * Reboot:
    <pre>
    sudo reboot
    </pre>
  * Log in with new hostname:
    <pre>
    ssh <i>admin</i>@<i>myserver</i>.local
    </pre>
  * Make sure everything is up-to-date:
    <pre>
    sudo apt update && sudo apt -y upgrade
    </pre>
  * Reboot:
    <pre>
    sudo reboot
    </pre>

## Adding external storage devices
  * Plug in both USB thumb drives and verify that they are recognized as `/dev/sda` and `/dev/sdb`:
    <pre>
    lsblk
    </pre>

  * Install the RAID software manager:
    <pre>
    sudo apt-get install mdadm
    </pre>
  * Create RAID1 array (e.g. <code><i>md0</i></code>):
  * <pre>
    sudo mdadm --create --verbose /dev/<i>md0</i> --level=1 --raid-devices=2 /dev/sda /dev/sdb
    </pre>
  * Check progress:
    <pre>
    cat /proc/mdstat
    </pre>
  * Create a filesystem on the RAID1 array:
    <pre>
    sudo mkfs.ext4 -F /dev/<i>md0</i>
    </pre>
  * Create a mount point to attach the filesystem (e.g. <code><i>md0</i></code>):
    <pre>
    sudo mkdir -p /mnt/<i>md0</i>
    </pre>
  * Mount the filesystem:
    <pre>
    sudo mount /dev/<i>md0</i> /mnt/<i>md0</i>
    </pre>
  * Verify the new space is available:
    <pre>
    df -h -x devtmpfs -x tmpfs
    </pre>
  * Make sure the filesystem is mounted whenever you boot:
    <pre>
    sudo echo '/dev/<i>md0</i> /mnt/<i>md0</i> ext4 defaults,noatime 0 1' | sudo tee -a /etc/fstab
    </pre>
  * Make sure your raid array starts up correctly on boot:
    <pre>
    sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf
    </pre>
  * Reboot:
    <pre>
    sudo reboot
    </pre>
