#!/bin/bash
set -e

# VNC default no password
export X11VNC_AUTH="-nopw"

# Create the SUT in DAI
python3 /create_sut.py

# override above if VNC_PASSWORD env var is set (insecure!)
if [[ "$VNC_PASSWORD" != "" ]]; then
  export X11VNC_AUTH="-passwd $VNC_PASSWORD"
fi

# make sure .config dir exists
mkdir -p /home/chrome/.config
chown chrome:chrome /home/chrome/.config

# set sizes for both VNC screen & Chrome window
: ${VNC_SCREEN_SIZE:='1920x1200'}
IFS='x' read SCREEN_WIDTH SCREEN_HEIGHT <<< "${VNC_SCREEN_SIZE}"
export VNC_SCREEN="${SCREEN_WIDTH}x${SCREEN_HEIGHT}x24"
export CHROME_WINDOW_SIZE="${SCREEN_WIDTH},${SCREEN_HEIGHT}"

export CHROME_OPTS="${CHROME_OPTS_OVERRIDE:- --user-data-dir --window-position=0,0 --force-device-scale-factor=1 --disable-dev-shm-usage --no-first-run --test-type --no-sandbox}"

exec "$@"
