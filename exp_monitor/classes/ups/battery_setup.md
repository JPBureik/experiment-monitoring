# Eaton 5PX UPS Integration

# Table of Contents
* [Recommended Hardware](#recommended-hardware)
* [Setting up the Gigabit Network Card for SNMP](#setting-up-the-gigabit-network-card-for-snmp)
* [Setting up the server for SNMP](#setting-up-the-server-for-SNMP)

## Recommended Hardware
* [Eaton Gigabit Network Card](https://www.rexel.fr/frx/Cat%C3%A9gorie/R%C3%A9seau-informatique/Onduleur/Accessoires-onduleur/Gigabit-Network-Card/EONNETWORK-M2/p/71711345?showBackLink=false)

#### The instructions below are given for a Linux command line. SSH will generally work from the command prompt on Windows 10 and newer. Replace text in *italitcs*.

## Setting up the Gigabit Network Card for SNMP
* Install the Eaton Gigabit Network Card. Declare its IP <i>battery_ip</i> address with the SI so that it can communicate on the IOGS network.
* Login via the web interface and go to `Settings`, then choose `SNMP`.
* Enable the `Activate SNMP` option.
* Enable `SNMP V3`.
* Edit the settings for the first `readonly` user in the `SNMP V3` section:
    - User name: exp_monitor
    - Enabled: Active
    - Access: Read only
    - Security: No Auth, No Priv
* Click on `Supported MIBs` and download the four files into `~/Downloads/eaton`.

## Setting up the server for SNMP
* Connect to <i>myserver</i>:
    <pre>
    ssh admin@<i>myserver</i>.local
    </pre>
* Install the required libraries:
    <pre>
    sudo apt-get install libsnmp-dev snmp-mibs-downloader
    sudo apt-get install gcc python-dev
    sudo apt install snmp
    pip3 install easysnmp
    </pre>
* Inspect the search paths of net-snmp:
    <pre>
    net-snmp-config --snmpconfpath
    </pre>
    This list should contain the path <pre>/home/<i>admin</i>/.snmp</i></pre>. Create a directory at this path and move the MIBs there:
    <pre>
    mkdir -p ~/.snmp/mibs
    </pre>
* On your personal machine, extract the downloaded .zip files:
    <pre>
    unzip ~/Downloads/eaton/*.zip
    </pre>
* Copy the MIBs to <i>myserver</i>:
    <pre>
    find ~/Downloads/eaton/ -name "*.txt" -type f -exec scp '{}' <i>admin</i>@<i>myserver</i>.local:/home/<i>admin</i>/.snmp/mibs ';'
    </pre>
    Don't worry about overwriting `EATON-OIDS.txt`, all three files of this name are identical.
* Edit the net-snmp configuration file to include the new MIBs:
    <pre>
    sudo nano /etc/snmp/snmp.conf
        mibs +EATON-ATS2-MIB
        mibs +EATON-SENSOR-MIB
        mibs +UPS-MIB
        mibs +EATON-EMP-MIB
        mibs +EATON-OIDS
        mibs +XUPS-MIB
    </pre>
* On your personal machine (within the IOGS network), make sure the SNMP communication is working:
    <pre>
    snmpwalk -v3 -u <i>exp_monitor</i> -l authNoPriv -a SHA-256 -A <i>battery_pw</i> <i>battery_ip</i>
    </pre>
    This should give a long list of all available MIBs with their polled values.