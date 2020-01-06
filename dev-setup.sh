#!/bin/sh

pip3 install -r requirements.txt -r requirements-dev.txt --user
pre-commit install
pre-commit autoupdate
chmod a+x update_tracker.py

if [ -d /run/user/1001/gvfs/smb-share:server=hassio,share=config/ ]; then
    ln -s /run/user/1001/gvfs/smb-share:server=hassio,share=config/ dev-config
fi
