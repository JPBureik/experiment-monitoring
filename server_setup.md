# Experiment Monitoring Server Setup

## Recommended Hardware

  * [Raspberry Pi 4B 8GB](https://fr.farnell.com/raspberry-pi/rpi4-modbp-8gb/raspberry-pi-4-model-b-cortex/dp/3369503)
  * [Micro SD Card 128GB](https://fr.farnell.com/sandisk/sdsqxcy-128g-gn6ma/extreme-pro-c10-microsdhc-128gb/dp/3410257)
  * [5V USB-C Power Supply](https://fr.farnell.com/raspberry-pi/sc0213/alimentation-rpi-usb-c-5-1v-3a/dp/3106941)
  * 2x [128GB USB thumb drive](https://www.amazon.fr/Integral-Fusion-Lecteur-Flash-Silver/dp/B018C5A0PE/ref=psdc_2908498031_t4_B07MDXBTL1)
  * [Cooling Case for RaspberryPi](https://www.amazon.fr/GeeekPi-Raspberry-Ventilateur-40X40X10mm-Dissipateurs/dp/B07XCKNM8J/ref=sr_1_6?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=boitier+raspberry+pi+4&qid=1625738015&sr=8-6)
  * PC with an SD card reader

#### The instructions below are given for a Linux command line. SSH will generally work from the command prompt on Windows 10 and newer. Replace text in *italitcs*.

## Preparing the RaspberryPi

  * In order to have internet access, declare the MAC address of the RaspberryPi at the [Service Info](https://ticket.institutoptique.fr/front/helpdesk.public.php?create_ticket=1), specifying explicitly that the new machine is a headless RaspberryPi.

  * [Download](https://www.raspberrypi.org/downloads/raspbian/) and install Raspberry Pi OS Lite on the SD card.

  * Add an SSH file to the boot SD card:
    <pre>
    touch boot/ssh
    </pre>
  * Put the RaspberryPi in its cooling case. Install it in the lab and connect the Ethernet and power cables. Then from any computer inside the IOGS network, get the RaspberryPi's IP address:
    <pre>
    ping raspberrypi.local
    </pre>
  * On your machine add ECDSA host key for RaspberryPi:
    <pre>
    ssh-keygen -f “/home/<i>user</i>/.ssh/known_hosts” -R “<i>IP</i>”p
    </pre>
  * SSH into the RaspberryPi with default password `raspberry`:
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
  * Reboot the RaspberryPi:
    <pre>
    sudo reboot
    </pre>
  * SSH into the RaspberryPi with the new password:
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

## Configuring the RaspberryPi
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
  * Add the SSH key to your QuantumGitLab account: In your web browser on the machine that you used to ssh into your RaspberryPi, go to `quantumgitserver.local`, enter your IOGS e-mail and your password. Then in the upper right hand corner click onto your icon and go to `Preferences`. From the column on the left hand side, choose `SSH keys`. Click on the `Key` text field and press `Ctrl+V` to paste the SSH key you've copied to your clipboard. Give it an appropriate `Title` (e.g. <i>MyServer</i>). Leave the `Expires at` field blank unless you have a reason to have your key expire at some point, then click `Add key`. You can now clone repositories on QuantumGitLab from <code><i>myserver</i></code>. You can use the same procedure to authorize <code><i>myserver</i></code> for GitHub connections.  
  * Install and configure Git:
    <pre>
    sudo apt-get install git
    git config --global user.email "<i>you</i>@<i>example.com</i>"
    git config --global user.name "<i>Your Name</i>"
    </pre>
    where <code><i>you</i>@<i>example.com</i></code> is the e-mail address you want associated with Git on <code><i>myserver</i></code>.
  * On your <b>desktop machine</b>, copy your SSH key to <code><i>myserver</i></code>:
    <pre>
    ssh-copy-id <i>admin</i>@<i>myserver</i>.local
    </pre>
    If you don't already have an SSH key on your desktop machine, repeat the steps above for generating a new SSH key and adding it to the ssh-agent.<br>
    From now on you can log into <code><i>myserver</i></code> without having to enter your user password just by using:
    <pre>
    ssh -X <i>admin</i>@<i>myserver</i>.local
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
  * Shortcut for the IOGS Palaiseau VPN (Linux only) on your <b>desktop machine</b>:
    <pre>
    sudo apt-get install expect
    nano ~/Documents/prog/expect/launcher
    &emsp; #!/bin/bash
    &emsp; cd /etc/openvpn/client && openvpn /etc/openvpn/client/PAL-VPN.ovpn
    nano ~/Documents/prog/expect/pvpn
    &emsp; #!/usr/bin/expect -f
    &emsp; set timeout -1
    &emsp; spawn ./launcher
    &emsp; expect "Enter Auth Username:"
    &emsp; send -- "<i>first</i>.<i>last</i>\n"
    &emsp; expect "Enter Auth Password:"
    &emsp; send -- "<i>my_passwd</i>\n"
    &emsp; interact
    nano ~/.bashrc
    &emsp; alias pvpn="cd ~/Documents/prog/expect && sudo ./pvpn"
    </pre>
    Now to launch the IOGS Palaiseau VPN all you need to do is open a terminal window and type `pvpn`. No need to re-enter username and password.
  * Shortcuts for the Shell on your <b>desktop machine</b>:
    - On Linux or Mac: Edit your SSH configuration file:
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
  * Shortcut for Grafana on your <b>desktop machine</b>:
    <pre>
    nano ~/.bashrc
    &emsp; alias grafana="ssh -L 8080:<i>myserver</i>.local:3000 <i>pasquano_user</i>@<i>pasquano_IP</i>"
    </pre>
    Now to access the Grafana interface from the outside, all you need to do is enable the IOGS Palaiseau VPN, open a terminal window, type `grafana` and then in your web browser go to `http://localhost:8080/`.

## Adding external storage devices
  * SSH back into <code><i>myserver</i></code>. Plug in both USB thumb drives and verify that they are recognized as `/dev/sda` and `/dev/sdb`:
    <pre>
    lsblk
    </pre>

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
  * Verify that the data is being written into your database:
    <pre>
    influx -precision rfc3339
    USE <i>mydatabase</i>
    SELECT * FROM <i>myseries</i>
    EXIT
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
  * Edit the Grafana configuration file:
    <pre>
    nano /etc/grafana/grafana.ini
    &emsp; [smtp]
    &emsp; enabled = true
    &emsp; host = smtps.universite-paris-saclay.fr:465
    &emsp; user = <i>first</i>.<i>last</i>@institutoptique.fr
    &emsp; # If the password contains # or ; you have to wrap it with triple quotes. Ex """#password;"""
    &emsp; password = <i>iogs_mail_pwd</i>
    &emsp; ;cert_file =
    &emsp; ;key_file =
    &emsp; skip_verify = true
    &emsp; from_address = grafana@<i>experiment_name</i>.institutoptique.fr
    &emsp; from_name = Grafana <i>Experiment Name</i>
    </pre>
    __Note about the notification e-mail server:__<br>
    The network infrastructure at IOGS is currently set up in such a way that SMTP connections are only allowed for one host, that is `smtps.universite-paris-saclay.fr` on port `465`. The only type of e-mail address available for Grafana notifications is thus your IOGS e-mail address. It is important to note, however, that your e-mail account will be blocked by the <i>Service Info</i> when they detect that you send a large volume of e-mails (several dozens within less than an hour); keep this in mind when setting up the automatic alerts in Grafana.<br>
    In general, you can always test whether or not the SMTP server of your choice is available from within your current network by using:
    <pre>
    sudo apt-get install telnet
    telnet <i>smtp_server</i> <i>port</i>
    </pre>
    where <code><i>smtp_server</i></code> could be e.g. <code>smtp.gmail.com</code> and the port will be either `465` (SSL) or `587` (TLS/STARTTLS).
  * Set up a new Grafana notification channel:<br>
    In the Grafana web interface, click the `Alerting` bell icon on the left hand side, choose `Notification channels`, then click on `Add channel`. Enter the following:
    <pre>
    Name: E-Mail Notification
    Type: E-Mail
    Addresses: <i>all addresses that are to be notified in case of alerts, separated by ";"</i>
    </pre>
    Check the `Default` and `Include image` options in `Notification settings`, then click on `Test`. All recipients specified in `Addresses` should have received a test e-mail.
  * Set up alerts:<br>
    From your dashboard, choose a time series graph, click on `Edit` and then on `Alert`. Enter the conditions under which you want to receive an automatic alert e-mail for that measurement, and how to handle no data or error situations. Enter a message describing the alert situation, then click on `Test rule`. If the threshold set for the alert is below the current value, the fourth line should read:
    <pre>
    condition evals: "false = false"
    </pre>
    Now change the threshold value to be below your current value and re-execute the rule test. The same line should now read:
    <pre>
    condition evals: "true = true"
    </pre>
    Change the threshold value back to the alert threshold, then on the upper right hand side click on `Apply` and save the dashboard by clicking on the save icon on the upper right hand side of the dashboard.<br>
    You can find an overview of all your alert rules by clicking on the `Alerting` bell icon and then choosing `Alert rules`.

## Backup to oa-data
Mount oa-data:
sudo mount -t cifs -o user='jan-philipp.bureik',sec=ntlm,workgroup=domain.iogs,vers=1.0 //oa-data.domain.iogs/Lattice\ Gases/pc_backups /mnt/oa-data
Backup all hard drives (e.g. /dev/sda):
sudo dd if=/dev/sda bs=64K conv=noerror,sync status=progress | gzip -c > /mnt/oa-data/backup_heliumserver_2021_04_29/backup_heliumserver_sda_2021_04_29.img.gz
Write shell script for this.
