#!/bin/bash

# Deploy experiment monitoring software to HeliumServer.

# Check for remote flag:
target="git@heliumserver.local"
while getopts "r" opt; do
  case $opt in
    r) target="git@heliumserver.remote"
    ;;
  esac
done

cd /home/jp/Documents/prog/work/exp_monitor
tar -czf exp_monitor.tar.gz *.p*
scp exp_monitor.tar.gz $target:/mnt/md1
rm exp_monitor.tar.gz
ssh $target << EOF
    cd /mnt/md1/exp_monitor
    if test -f "../exp_monitor.tar.gz"; then
        rm -r *
        tar -xzf ../exp_monitor.tar.gz
        rm ../exp_monitor.tar.gz
    fi
EOF
echo "Deployed experiment monitoring software to HeliumServer."
