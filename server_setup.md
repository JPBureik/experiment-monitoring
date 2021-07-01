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

## Access from outside the IOGS network
  * By default, <code><i>myserver</i></code> is set up for local access only for security reasons. If port forwarding is used to ssh-tunnel to it directly, you have to consider security in terms of firewalls and attempted access surveillance.

  * Instead, in order to connect from the outside, it is suggested to make use of already existing infrastructure and use a machine for which the ports have already been opened (e.g. <code><i>Pasquano</i></code>) as an SSH proxy.
  * The Palaiseau VPN has to be enabled for outside access. This guarantees only IOGS staff will be able to access <code><i>myserver</i></code> from the outside.
  * To jump through <code><i>Pasquano</i></code> to <code><i>myserver</i></code> use the `J` flag for `ssh`:
    <pre>
    ssh -J <i>pasquano_user</i>@<i>pasquano_IP</i> <i>admin</i>@<i>myserver</i>.local
    </pre>
  * And the `o` flag for `scp`:
    <pre>
    scp -o 'ProxyJump <i>pasquano_user</i>@<i>pasquano_IP</i>' <i>test.py</i> <i>admin</i>@<i>myserver</i>.local:/mnt/<i>md0</i>
  * Shortcuts:
    - On Linux or Mac: Edit your SSH configuration file (e.g. using `nano`):
      <pre>
      sudo nano ~/.ssh/config
      </pre>
      At the bottom add:
      <pre>
      # SSH tunnel to <i>myserver</i> via <i>Pasquano</i>
        Host <i>pasquano</i>
          User <i>pasquano_user</i>
          HostName <i>pasquano_IP</i>
        Host <i>myserver</i>.remote
          HostName <i>myserver</i>.local
          ProxyJump <i>pasquano</i>
      </pre>
      You can now use standard syntax for `ssh` and `scp` commands:
      *  Opening an ssh session:
          <pre>
          ssh <i>admin</i>@<i>myserver</i>.remote
          </pre>
      * Copying from local to distant:
        <pre>
        scp ~/<i>folder</i>/<i>test.py</i> <i>admin</i>@<i>myserver</i>.remote:/mnt/<i>md0</i>/<i>folder</i>/<i>test.py</i>
    - On Windows:
      [Download](https://sourceforge.net/projects/xming/) and install `Xming`.
      Open `PuTTY`:
      <pre>
      Session:
        &emsp; Host Name: <i>myserver</i>.local
        &emsp; Port: 22
      Connection:
        &emsp; Data:
        &emsp; &emsp; Auto-login username: <i>admin</i>
        &emsp; Proxy:
        &emsp; &emsp; Proxy hostname: <i>pasquano_IP</i>
        &emsp; &emsp; Port: 22
        &emsp; &emsp; Username: <i>pasquano_user</i>
        &emsp; &emsp; Password: <i>pasquano_password</i>
        &emsp; &emsp; Telnet command, or local proxy command: plink.exe %user@%proxyhost -pw %pass -P %proxyport -nc %host:%port
        &emsp; SSH:
        &emsp; &emsp; Enable X11 forwarding: Yes
      Session:
        &emsp; Saved Sessions: <i>myserver</i>
        &emsp; Save
      Open
      </pre>
      You can now copy files from the command prompt using:
      <pre>
      pscp -load <i>myserver</i> C:\<i>folder</i>/<i>test</i> <i>myserver</i>.local:/mnt/<i>md0</i>
  * Setup SSH keys:
    <pre>
    ssh-keygen -t ed25519 -C "your_email@example.com"
    </pre>
