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

  * [Download](https://www.raspberrypi.org/downloads/raspbian/) and install Raspberry Pi OS Lite on the SD card

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
  * Disable root login:
    <pre>
    sudo passwd -l root
    </pre>

## Configuring the RPI
  * Set the host name of your server:<br>
      Enter configuration menu:
    <pre>
    sudo raspi-config
    </pre>

  * System options:
    <pre>
    S4 Hostname
      &emsp; <i>myserver</i>
    </pre>
    Select `Finish` then `Yes` to reboot.
  * Log in with new hostname:
    <pre>
    ssh <i>admin</i>@<i>myserver</i>.local
    </pre>
  * Set the locales corresponding to your region and languages of choice:
    - Login as root:
      <pre>
      sudo su
      </pre>
    - Uncomment the languages of your choice in <code>/etc/locale.gen</code>, e.g. English and French:
      <pre>
      nano /etc/locale.gen
        &emsp; en_GB ISO-8859-1
        &emsp; en_GB.UTF-8 UTF-8
        &emsp; en_US ISO-8859-1
        &emsp; en_US.UTF-8 UTF-8
        &emsp; fr_FR ISO-8859-1
        &emsp; fr_FR.UTF-8 UTF-8
      </pre>
    - Generate the new locales and logout of root:
      <pre>
      locale-gen
      exit
      </pre>
  * Set system time for InfluxDB time stamps:
    <pre>
    sudo timedatectl set-timezone Europe/Paris
    </pre>
  * Make sure everything is up-to-date:
    <pre>
    sudo apt update && sudo apt -y upgrade
    </pre>
  * To enable X11 forwarding, install the X_Windows package:
    <pre>
    sudo apt install xorg
    </pre>
  * Check correct value for `DISPLAY` environment parameter:
    <pre>
    echo $DISPLAY
    </pre>
    This should return <code>localhost:10.0</code>. If not, set the `DISPLAY` parameter manually:
    <pre>
    export DISPLAY=localhost:10.0
    </pre>
    Now you can start up remote applications but forward the application display to your local machine by using the `X` flag with `ssh`. Log back in with X11 forwarding enabled:
    <pre>
    exit
    ssh -X <i>admin</i>@<i>myserver</i>.local
    </pre>
    This also enables the use of tools such as `xclip` that allow you to copy a command line output to the clipboard. This is useful for setting up SSH keys.
  * Install `xclip`:
    <pre>
    sudo apt install xclip
    </pre>
  * Create an SSH key with your IOGS e-mail address:
    <pre>
    ssh-keygen -t rsa -b 4096 -C "<i>first</i>.<i>last</i>@institutoptique.fr"
    </pre>
    Press `Enter` to use the default options for filepath and passphrase.
  * Add the SSH key to the ssh-agent:
    <pre>
    eval "$(ssh-agent -s)"
    ssh-add ~/.ssh/id_rsa
    </pre>
  * Copy the public key to your clipboard:
    <pre>
    cat ~/.ssh/id_rsa.pub | xclip -sel clip
    </pre>
  * Add the SSH key to your QuantumGitLab account: In your web browser go to `quantumgitserver.local`, enter your IOGS e-mail and your password. Then in the upper right hand corner click onto your icon and go to `Preferences`. From the column on the left hand side, choose `SSH keys`. Click on the `Key` text field and press `Ctrl+V` to paste the SSH key you've copied to your clipboard. Give it an appropriate `Title` (e.g. <i>MyServer</i>). Leave the `Expires at` field blank unless you have a reason to have your key expire at some point, then click `Add key`. You can now clone repositories on QuantumGitLab from <code><i>myserver</i></code>. You can use the same procedure to authorize <code><i>myserver</i></code> for GitHub connections.  
  * Install Git:
    <pre>
    sudo apt-get install git
    </pre>
  * On your <b>desktop machine</b>, copy your SSH key to <code><i>myserver</i></code>:
    <pre>
    ssh-copy-id <i>admin</i>@<i>myserver</i>.local
    </pre>
    If you don't already have an SSH key on your desktop machine, repeat the steps above for generating a new SSH key and adding it to the ssh-agent.<br>
    From now on you can log into <code><i>myserver</i></code> without having to enter your user password just by using:
    <pre>
    ssh -X <i>admin</i>@<i>myserver</i>.local
    </pre>

## Adding external storage devices
  * Plug in both USB thumb drives and verify that they are recognized as `/dev/sda` and `/dev/sdb`:
    <pre>
    lsblk
    </pre>

<!--
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
  * <b>Important</b>: From this point forward it is no longer recommended to use `sudo reboot` to reboot the server, as this can lead to a failure during boot that can only be solved by reformatting the SD card. Instead, use
    <pre>
    sudo shutdown -h now
    </pre>
    then unplug the power cable once the server has shut down and plug back in to start back up.
-->
  * Create a filesystem on both drives:
    <pre>
    sudo mkfs.ext4 -F /dev/sda
    sudo mkfs.ext4 -F /dev/sdb
    </pre>
  * Create mount points to attach the filesystems (e.g. <code>code</code> and <code>data</code>):
    <pre>
    sudo mkdir -p /mnt/code
    sudo mkdir -p /mnt/data
    </pre>
  * Mount the filesystems:
    <pre>
    sudo mount /dev/sda /mnt/code
    sudo mount /dev/sdb /mnt/data
    </pre>
  * Verify the new space is available:
    <pre>
    df -h -x devtmpfs -x tmpfs
    </pre>
  * Make sure the filesystems are mounted whenever you boot:
    <pre>
    sudo echo '/dev/sda /mnt/code ext4 defaults,noatime 0 1' | sudo tee -a /etc/fstab
    sudo echo '/dev/sdb /mnt/data ext4 defaults,noatime 0 1' | sudo tee -a /etc/fstab
    </pre>
  * Give write permissions:
    <pre>
    cd /mnt
    sudo chmod a+w code
    sudo chmod a+w data
    </pre>
  * Reboot and verify filesystems are mounted:
    <pre>
    sudo reboot
    ssh <i>admin</i>@<i>myserver</i>.local
    lsblk</pre>

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
      *  Opening an SSH session:
          <pre>
          ssh <i>admin</i>@<i>myserver</i>.remote
      * Copying from local to distant:
        <pre>
        scp ~/<i>folder</i>/<i>test.py</i> <i>admin</i>@<i>myserver</i>.remote:/mnt/<i>md0</i>/<i>folder</i>/<i>test.py</i>
    - On Windows:
      [Download](https://sourceforge.net/projects/xming/) and install `Xming`.
      Open `PuTTY`:
      - Session:
        <pre>
        Host Name: <i>myserver</i>.local
        Port: 22
      - Connection:
        <pre>
        Data:
        &emsp; Auto-login username: <i>admin</i>
        Proxy:
        &emsp; Proxy hostname: <i>pasquano_IP</i>
        &emsp; Port: 22
        &emsp; Username: <i>pasquano_user</i>
        &emsp; Password: <i>pasquano_password</i>
        &emsp; Telnet command, or local proxy command: plink.exe %user@%proxyhost -pw %pass -P %proxyport -nc %host:%port
      - SSH:
        <pre>
        Enable X11 forwarding: Yes
      - Session:
        <pre>
        Saved Sessions: <i>myserver</i>
        Save
        </pre>
      - Open<br>
      You can now copy files from the command prompt using:
      <pre>
      pscp -load <i>myserver</i> C:\<i>folder</i>/<i>test</i> <i>myserver</i>.local:/mnt/<i>md0</i>
      </pre>

## Installing InfluxDB and Grafana
  * Install InfluxDB and start the service:
    <pre>
    sudo curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
    sudo echo "deb https://repos.influxdata.com/ubuntu bionic stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
    sudo apt update
    sudo apt install influxdb
    sudo systemctl start influxdb
    </pre>

  * Install Grafana:
    <pre>
    wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
    echo "deb https://packages.grafana.com/oss/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
    sudo apt-get update
    sudo apt-get install -y grafana
    </pre>
  * Edit the `[panels]` section in the Grafana settings file:
    <pre>
    sudo nano /etc/grafana/grafana.ini
    &emsp; [panels]
    &emsp; enable_alpha = false
    </pre>
  * Enable and start the Grafana server:
    <pre>
    sudo /bin/systemctl enable grafana-server
    sudo /bin/systemctl start grafana-server
    </pre>
  * Start Grafana automatically after reboot:
    <pre>
    sudo nano /etc/rc.local
    &emsp; sudo service grafana-server restart
    </pre>

## Setting up the continuous data acquisition:
  * Download the Experiment Monitoring software:
    <pre>
    cd /mnt/code
    git clone -o quantumgitserver git@quantumgitserver.local:helium-lattice/experiment-monitoring.git
    </pre>
  * Install the required Python libraries:
    <pre>
    sudo apt install python3-pip
    sudo apt-get install python-dev libatlas-base-dev libopenjp2-7 libtiff5
    pip3 install numpy influxdb Phidget22 pyserial scipy matplotlib
    </pre>
  * Install Phidgets drivers:
    <pre>
    cd /tmp
    wget https://www.phidgets.com/downloads/phidget22/libraries/linux/libphidget22.tar.gz
    tar zxvf libphidget22.tar.gz
    cd libphidget22-* <i>(auto-complete with Tab)</i>
    ./configure
    make
    sudo make install
    </pre>
    Add  `/usr/local/lib` to the system-wide library path:
    <pre>
    sudo su -
    echo /usr/local/lib >> /etc/ld.so.conf && sudo ldconfig
    exit
    </pre>
    Extend the USB access rules:
    <pre>
    sudo usermod -a -G dialout $USER
    sudo cp plat/linux/udev/99-libphidget22.rules /etc/udev/rules.d
    sudo udevadm control --reload
    sudo reboot
    </pre>
    Verify the Phidgets are seen by your USB interface:
    <pre>
    ssh -X <i>admin</i>@<i>myserver</i>.local
    dmesg | tail
    </pre>
  * Test the Phidgets drivers with Python:
    <pre>
    cd /tmp
    wget https://www.phidgets.com/downloads/phidget22/examples/python/Manager/Phidget22_HelloWorld_Python_Ex.zip
    unzip Phidget22_HelloWorld_Python_Ex.zip
    python3 HelloWorld.py
    </pre>
    This last command should list all of your connected Phidgets.
  * Set up the InfluxDB database (e.g. <i>mydatabase</i>):
    <pre>
    influx -precision rfc3339
    CREATE DATABASE <i>mydatabase</i>
    </pre>
    Add this name in the config file of the Experiment Monitoring Python package and sync with QuantumGitServer:
    <pre>
    nano /mnt/code/experiment-monitoring/config.py
      &emsp; database_name = '<i>mydatabase</i>'
    git add .
    git commit -m "Specified influxdb database name"
    git push quantumgitserver master
    </pre>
  * Set up the Experiment Monitoring software for your experiment:
    <pre>
    nano /mnt/code/experiment-monitoring/config.py
    </pre>
  * Manually execute one data acquisition cycle to check for errors:
    <pre>
    python3 /mnt/code/experiment-monitoring/influxdb_write.py
    </pre>
  * If the data acquisition script executes without any errors, setup its automatic continuous execution via a Linux service:
    <pre>
    cd /lib/systemd/system
    sudo nano exp_monitor.service
      &emsp; [Unit]
      &emsp; Description=Experiment Monitoring Software
      &emsp; After=multi-user.target

      &emsp; [Service]
      &emsp; Type=simple
      &emsp; ExecStart=/usr/bin/python3 /mnt/code/exec.py
      &emsp; Restart=always
      &emsp; RestartSec=15s         
      &emsp; User=admin   

      &emsp; [Install]
      &emsp; WantedBy=multi-user.target
    sudo chmod 644 /lib/systemd/system/exp_monitor.service
    sudo chmod +x /mnt/code/experiment-monitoring/exec.py
    sudo systemctl daemon-reload
    sudo systemctl enable exp_monitor.service
    sudo systemctl start exp_monitor.service
    </pre>
    Now you can start/stop/restart the execution of the Experiment Monitoring software using:
    <pre>
    sudo systemctl start/stop/restart exp_monitor.service
    </pre>
    You can relaunch the daemon using:
    <pre>
    sudo systemctl daemon-reexec
    </pre>
    You can check the status of the execution using:
    <pre>
    sudo systemctl status exp_monitor.service
    </pre>
    You can check the execution log using:
    <pre>
    sudo journalctl -f -u exp_monitor.service
    </pre>

## Setting up the data monitoring:
  * Access the Grafana interface from a web browser by navigating to:
    <pre>
    <i>myserver</i>.local:3000
    </pre>
    The user name and password for the first connection are by default both `admin`. Change the password as prompted immediately after the first login.<br>
    Click on your user icon on the lower left hand side to edit your profile preferences. Then go to the settings page from the icon on the upper right hand side. Change the `Name` and `Description` according to your situation. Under `Auto refresh` add the following options:
    <pre>
    5s,10s,30s,1m,5m,15m,30m,1h,2h,1d
    </pre>
  * Add a data source from the configuration icon on the left hand side. Choose `InfluxDB`, then enter:
    <pre>
    HTTP
    &emsp; URL: http://localhost:8086/
    InfluxDB Detaisl
    &emsp; Database: <i>mydatabase</i>
    </pre>
    Click `Save & Test`.
  * Create a new dashboard from the `+` sign on the left hand side. Save it and name it according to your situation. Add a new panel from the icon on the upper right hand side. Choose `Add an empty panel`, then enter the following to monitor the measurement series <code><i>myseries</i></code> as specified in <code>/mnt/code/experiment-monitoring/config.py</code>:
    <pre>
    Data source: InfluxDB
    FROM <i>myseries</i> WHERE
    SELECT field(value)
    GROUP BY
    ORDER BY TIME ascending
    </pre>
    On the right hand side, enter the name of <code><i>myseries</i></code> and its description in the corresponding fields. Add its unit below `Standard options`, then click `Apply` and `Save`. You can add multiple time series in the same graph by adding another query (`B`) on the lower left hand side. On the upper right hand side, choose the time interval specified in <code>/mnt/code/experiment-monitoring/config.py</code> for the Grafana interface to automatically update. To add a gauge that displays the current value, proceed similarly but choose `Gauge` from the dropdown menu on the upper right hand side and in the `SELECT` row enter:
    <pre>
    SELECT field(value) last()
    </pre>

## Setting up automatic alerts


## Backup to oa-data
Mount oa-data:
sudo mount -t cifs -o user='jan-philipp.bureik',sec=ntlm,workgroup=domain.iogs,vers=1.0 //oa-data.domain.iogs/Lattice\ Gases/pc_backups /mnt/oa-data
Backup all hard drives (e.g. /dev/sda):
sudo dd if=/dev/sda bs=64K conv=noerror,sync status=progress | gzip -c > /mnt/oa-data/backup_heliumserver_2021_04_29/backup_heliumserver_sda_2021_04_29.img.gz
Write shell script for this.
