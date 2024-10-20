#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cat << EOF > lowerer.service
[Unit]
Description=Python instance starting the screen lowerer
Requires=graphical.target

[Service]
User=$USER
Environment="DISPLAY=:0"
WorkingDirectory=/usr/bin
Environment="PATH=$SCRIPT_DIR/env/bin"
ExecStart=$SCRIPT_DIR/env/bin/python $SCRIPT_DIR/lowerer.py
EOF
#mkdir -p $HOME/.config/systemd/user/
sudo -k ln -sf $SCRIPT_DIR/lowerer.service /etc/systemd/system/lowerer.service
sudo chmod ugo+w /sys/class/backlight/*/brightness
sudo systemctl daemon-reload
echo "Run \"sudo systemctl start lowerer\" to start the lowerer service"