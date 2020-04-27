#!/bin/sh

pip3 install pre-commit
pip3 install -r requirements.txt -r requirements-dev.txt --user
pre-commit install
pre-commit autoupdate
chmod a+x update_tracker.py

CONFIG=/run/user/$(id -u)/gvfs/smb-share:server=hassio,share=config/
if [ -d "$CONFIG" ] && [ ! -e dev-config ]; then
    ln -s "$CONFIG" dev-config
fi
