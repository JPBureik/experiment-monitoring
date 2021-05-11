#!/bin/bash

# Update calibration: Pull ->  run calib.py -> push

git pull origin master
python3 calib.py
git add calib.p
git commit -m "Calib update"
git push origin master