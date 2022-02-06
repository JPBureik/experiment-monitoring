# Experiment Monitoring Server Setup

# Table of Contents
  * [Recommended Hardware](#recommended-hardware)
  * [Preparing the RaspberryPi](#preparing-the-raspberrypi)
  * [Configuring the RaspberryPi](#configuring-the-raspberrypi)
  * [Access from outside the IOGS network](#access-from-outside-the-iogs-network)
  * [Adding external storage devices](#adding-external-storage-devices)
  * [Installing InfluxDB and Grafana](#installing-influxdb-and-grafana)
  * [Setting up the continuous data acquisition](#setting-up-the-continuous-data-acquisition)
  * [Setting up automatic backups](#setting-up-automatic-backups)
  * [Setting up the data monitoring](#setting-up-the-data-monitoring)
  * [Setting up automatic alerts](#setting-up-automatic-alerts)
  * [Known bugs and problems](#known-bugs-and-problems)

## Recommended Hardware

### Server
  * [Raspberry Pi 4B 8GB](https://fr.farnell.com/raspberry-pi/rpi4-modbp-8gb/raspberry-pi-4-model-b-cortex/dp/3369503)
  * [Micro SD Card 128GB](https://fr.farnell.com/sandisk/sdsqxcy-128g-gn6ma/extreme-pro-c10-microsdhc-128gb/dp/3410257)
  * [5V USB-C Power Supply](https://fr.farnell.com/raspberry-pi/sc0213/alimentation-rpi-usb-c-5-1v-3a/dp/3106941)
  * 2x [128GB USB thumb drive](https://www.amazon.fr/Integral-Fusion-Lecteur-Flash-Silver/dp/B018C5A0PE/ref=psdc_2908498031_t4_B07MDXBTL1)
  * [Cooling Case for RaspberryPi](https://www.amazon.fr/GeeekPi-Raspberry-Ventilateur-40X40X10mm-Dissipateurs/dp/B07XCKNM8J/ref=sr_1_6?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=boitier+raspberry+pi+4&qid=1625738015&sr=8-6)
  * PC with an SD card reader

### Temperature Sensing (opt.)
  * [4x Thermocouple Phidget](https://www.phidgets.com/?tier=3&catid=14&pcid=12&prodid=1215)
  * [VINT Hub Phidget](https://www.phidgets.com/?tier=3&catid=2&pcid=1&prodid=1202)
  * [Phidget Cable](https://www.phidgets.com/?tier=3&catid=30&pcid=26&prodid=154)
  * [K-Type Teflon Bead Probe Thermocouple](https://www.phidgets.com/?tier=3&catid=14&pcid=12&prodid=727)
  * [USB Cable](https://fr.rs-online.com/web/p/cables-usb/1828494)

### Analog Sensing (opt.)
  * [Arduino Due](https://store.arduino.cc/arduino-due)
  * [Arduino Ethernet Shield 2](https://store.arduino.cc/arduino-ethernet-shield-2)
  * [5V Power Supply](https://fr.farnell.com/xp-power/vel12us120-eu-ja/adaptateur-ac-dc-12v-1a/dp/2524421)
  * [3.3V Zener Diodes](https://fr.farnell.com/nexperia/bzx79-c3v3/diode-zener-500mw-3-3v/dp/1097229?MER=sy-me-pd-mi-alte)

### Eaton 5PX UPS Integration (opt.)
* [Eaton Gigabit Network Card](https://www.rexel.fr/frx/Cat%C3%A9gorie/R%C3%A9seau-informatique/Onduleur/Accessoires-onduleur/Gigabit-Network-Card/EONNETWORK-M2/p/71711345?showBackLink=false)


#### The instructions below are given for a Linux command line. SSH will generally work from the command prompt on Windows 10 and newer. Replace text in *italitcs*.

## Preparing the RaspberryPi

  * In order to have internet access, declare the MAC address of the RaspberryPi at the [Service Info](https://ticket.institutoptique.fr/front/helpdesk.public.php?create_ticket=1), specifying explicitly that the new machine is a headless RaspberryPi.

  * [Download](https://www.raspberrypi.org/downloads/raspbian/) and install Raspberry Pi OS Lite on the SD card.

  * Add an SSH file to the boot SD card:
    <pre>
    touch boot/ssh
    </pre>
  * Put the RaspberryPi in its cooling case. Install it in the lab and connect the Ethernet and power cables. Plug in both USB thumb drives. Then from any computer inside the network, get the RaspberryPi's IP address:
    <pre>
    ping raspberrypi.local
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
  * SSH into the RaspberryPi with the new root password:
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
  * Disable root login:
    <pre>
    sudo passwd -l root
    </pre>

## Configuring the RaspberryPi
  * Set the host name of your server:<br>
    - Enter configuration menu:
      <pre>
      sudo raspi-config
      </pre>
    - System options:
      <pre>
      S4 Hostname
        &emsp; <i>myserver</i>
      </pre>
    - Select `Finish` then `Yes` to reboot.
  * Log in with new hostname:
    <pre>
    ssh <i>admin</i>@<i>myserver</i>.local
    </pre>
  * Install and configure Git:
    <pre>
    sudo apt-get install git -y
    git config --global user.email "<i>you</i>@<i>example.com</i>"
    git config --global user.name "<i>Your Name</i>"
    </pre>
    where <code><i>you</i>@<i>example.com</i></code> is the e-mail address you want associated with Git on <code><i>myserver</i></code>.

## Adding external storage devices
  * Plug in both USB thumb drives and verify that they are recognized as `/dev/sda` and `/dev/sdb`:
    <pre>
    lsblk
    </pre>

  * Create a filesystem on both drives:
    <pre>
    sudo mkfs.ext4 -F /dev/sda
    sudo mkfs.ext4 -F /dev/sdb
    </pre>
  * Create mount points called <code>code</code> and <code>data</code> to attach the filesystems to:
    <pre>
    sudo mkdir /mnt/code /mnt/data
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
    sudo chmod +w /mnt/code
    sudo chmod +w /mnt/data
    </pre>
  * Reboot and verify filesystems are mounted:
    <pre>
    sudo reboot
    ssh <i>admin</i>@<i>myserver</i>.local
    lsblk</pre>

## Installing the Experiment Monitoring package
  * Clone the repository from GitHub:
    <pre>
    cd /mnt/code
    git clone -o github https://github.com/JPBureik/experiment-monitoring.git
    </pre>
  * Switch to root to run the server setup script and enter a name for the InfluxDB database when prompted (e.g. <i>mydatabase</i>):
    <pre>
    sudo su -
    /mnt/code/experiment-monitoring/server_setup/server_setup.sh
    </pre>
    The server will reboot after completing the setup.
  * Connect the Phidgets and test their drivers:
    <pre>
    ssh <i>admin</i>@<i>myserver</i>.local
    /mnt/code/experiment-monitoring/tests/test_phidgets.sh
    </pre>
    This should list all of your connected Phidgets.

## Setting up the continuous data acquisition
  * Connect all of the devices that you want to monitor.
  * To set up the Experiment Monitoring software for your experiment, instantiate all sensor objects as subclasses of the `Sensor` class in the main configuration file:
    <pre>
    nano /mnt/code/experiment-monitoring/src/expmonitor/config.py
    </pre>
    Any subclass of the `Sensor` class needs to overwrite all of its `abstractmethods` and specify all of its `__init__` arguments. See the `README` for a list of existing driver classes.
  * Manually execute some (e.g. <i>5</i>) data acquisition cycles to check for errors:
    <pre>
    python3 /mnt/code/experiment-monitoring/src/expmonitor/exec.py t v <i>5</i>
    </pre>
    Note that the argument after the the script filepath sets the number of executions of the loop. The `t` and `v` flags enable timing and exception traceback to `stdout`.
  * Verify that the data is being written into your database:
    <pre>
    influx -precision rfc3339
    USE <i>mydatabase</i>
    SHOW SERIES
    SELECT * FROM <i>myseries</i>
    EXIT
    </pre>
  * If the data acquisition script executes without any errors, setup its automatic continuous execution via a Linux service:
    <pre>
    sudo systemctl enable expmonitor.service
    sudo systemctl start expmonitor.service
    </pre>
    Now you can start/stop/restart the execution of the Experiment Monitoring software using:
    <pre>
    sudo systemctl start/stop/restart expmonitor.service
    </pre>
    You can relaunch the daemon using:
    <pre>
    sudo systemctl daemon-reexec
    </pre>
    You can check the status of the execution using:
    <pre>
    sudo systemctl status expmonitor.service
    </pre>
    You can check the execution log using:
    <pre>
    sudo journalctl -f -u expmonitor.service
    </pre>

## Setting up automatic backups
  It is recommended that you set up automatic backups for <i>myserver</i>. If you're a member of the Quantum Gases group at IOGS, you can use your share on our NAS `OA-DATA`. Otherwise, replace <code><i>oa-data-share</i></code> with your own backup target.
  * On your <code><i>oa-data_share</i></code> create a directory <code>pc_backups</code> and therein one for <code><i>myserver</i></code>. On <code><i>myserver</i></code> create a mount point for <code><i>oa-data_share</i></code>:
    <pre>
    mkdir /mnt/oa-data
    </pre>

  * Set up your credentials file on <code><i>myserver</i></code>:
    <pre>
    sudo nano /root/.smbcredentials_oa-data
    &emsp; username=<i>first</i>.<i>last</i>
    &emsp; password=<i>oa-data_pwd</i>
    sudo chmod 600 /root/.smbcredentials_oa-data
    </pre>
  * Add <code><i>oa-data_share</i></code> to your <code>fstab</code>:
    <pre>
    sudo nano /etc/fstab
    &emsp; //oa-data.domain.iogs/<i>oa-data_share</i>/pc_backups/<i>myserver</i> /mnt/oa-data cifs vers=3.0,workgroup=domain.iogs,_netdev,credentials=/root/.smbcredentials_oa-data
    </pre>
  * Mount <code><i>oa-data_share</i></code>:
    <pre>
    sudo mount -a
    </pre>
  * Create a shell script for automatic backups:
    <pre>
    cd
    nano backup
    &emsp; #!/bin/sh
    &emsp; touch /home/<i>admin</i>/.backup_log_$(date +'%Y_%m_%d')
    &emsp; backup_dir=/mnt/<i>oa-data_share</i>/<i>myserver</i>_backup_$(date +'%Y_%m_%d')
    &emsp; mkdir -p $backup_dir/data
    &emsp; influxd backup -database <i>mydatabase</i> $backup_dir/data
    &emsp; sudo dd if=/dev/mmcblk0 bs=64K conv=noerror,sync | gzip -c > $backup_dir/mmcblk0.img.gz
    &emsp; find /mnt/oa-data/ -maxdepth 1 -type d -mtime +1 -exec rm -rf {} \;
    &emsp; find /home/<i>admin</i>/.backup_log_* -type f -mtime +1 -exec rm {} \;
    chmod u+x backup
    </pre>
  * Automate daily backups with `cron`:
    <pre>
    sudo crontab -e
    &emsp; 0 4 * * * /home/<i>admin</i>/backup >> /home/<i>admin</i>/.backup_log_`/usr/bin/date +\%Y_\%m_\%d` 2>&1
    </pre>
  * In case of problems with the backup, you can consult the backup log at <code>/home/<i>admin</i>/.backup_log_<i>2021_05_20</i></code>. By default the backups from the last two days are kept and the next oldest one is deleted after creation of a new one. The same applies to the backup logs. You can change this behavior by changing the argument of the `-mtime` flags in the `find` calls of the backup script.

## Setting up the data monitoring
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
    InfluxDB Details
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
  * If you want direct access to the database, use
    <pre>
    influx -precision rfc3339
    USE <i>mydatabase></i>
    </pre>
    * Get an overview of all your measurement series:
      <pre>
      SHOW SERIES
      </pre>
    * Show data from <i>myseries</i> for the last <i>5 minutes</i>, or for any time range you want:
      <pre>
      SELECT "value" FROM "<i>myseries</i>" WHERE time >= now() - <i>5m</i>
      SELECT "value" FROM "<i>myseries</i>" WHERE time >= '<i>2020-01-12T00:00:00-04:00</i>' AND time <  '<i>2020-01-13T00:00:00-04:00</i>'
      </pre>
    * If you want to delete specific data points from <i>myseries</i>, use:
      <pre>
      DELETE FROM "<i>my_series</i>" WHERE time = <i>1605871624000000000</i>
      </pre>
      where the time argument corresponds to the Unix time stamp of the data point. Start InfluxDB without the `-precision rfc3339` flag to show Unix time stamps for the time series instead of normal time stamps. The Python script `spike_filter.py` contains a static method on its class that converts Unix time to normal time.
    * If you ever want to delete a measurement series in InfluxDB, use:
      <pre>
      DROP MEASUREMENT <i>myseries</i>
      </pre>
    * If you want to rename a measurement series, stop the continuous data acquisition, then copy all data grouped by tags into a new series:
      <pre>
      SHOW TAG KEYS FROM <i>old_series</i>
      </pre>
      Example output:
      <pre>
      name: <i>old_series</i>
      tagKey
      ------
      <i>my_tag</i>
      </pre>
      Copy:
      <pre>
      SELECT * INTO <i>new_series</i> FROM <i>old_series</i> GROUP BY <i>my_tag</i>
      </pre>
      Example output:
      <pre>
      name: result
      time written
      ---- -------
      0    <i>227293</i>
      </pre>
      Check that <i>new_series</i> is present and that its data is identical with <i>old_series</i>:
      <pre>
      SHOW SERIES
      SELECT * FROM "<i>old_series</i>" WHERE time >= now() - 5m
      SELECT * FROM "<i>new_series</i>" WHERE time >= now() - 5m
      </pre>
      If comparison shows equivalence, change the data reference in the corresponding Grafana widgets to the new series.
      Change the data acquisition program so that its `json` output corresponds to the new database name.
      Restart the continuous execution of the data acquisition program and check that no new values are added to <i>old_series</i> in InfluxDB, and that data carries over from <i>new_series</i> and that new data is correctly written into <i>new_series</i>. If so, delete the old series in InfluxDB:
      <pre>
      DROP MEASUREMENT old_series
      </pre>
    * The experiment monitoring software suite also contains a Python script (`spike_filter.py`) that allows you to interact with InfluxDB and delete values, e.g. for spikes in acquired data.

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
    Check the `Default` option in `Notification settings`, then click on `Test`. All recipients specified in `Addresses` should have received a test e-mail.
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

## Known bugs and problems
  * The Grafana Image Renderer is not available for the ARM processor of the RaspberryPi. Therefore the alert e-mails do not contain a snapshot of the time series that causes the alert.
