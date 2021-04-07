#!/bin/bash

# Deploy experiment monitoring software to HeliumServer.

cd /home/jp/Documents/Work/prog/exp_monitor
tar -czf exp_monitor.tar.gz *.py 
scp exp_monitor.tar.gz git@heliumserver.local:/mnt/md1
rm exp_monitor.tar.gz
ssh git@heliumserver.local << EOF
    cd /mnt/md1/exp_monitor
    if test -f "../exp_monitor.tar.gz"; then
        rm -r *
        tar -xzf ../exp_monitor.tar.gz
        rm ../exp_monitor.tar.gz
    fi
EOF
echo "Deployed experiment monitoring software to HeliumServer."
