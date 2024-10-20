#!/bin/bash

sudo -k rm /etc/systemd/system/lowerer.service
rm lowerer.service
sudo chmod 600 /sys/class/backlight/*/brightness
sudo systemctl daemon-reload
echo "Lowerer destroyed, run \"./service_setup.sh\" to set it back up"