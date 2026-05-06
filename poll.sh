#!/bin/bash
while true; do
    socat - VSOCK-CONNECT:2:9999,timeout=0.1 >/dev/null 2>&1
    if [ 0 -eq 0 ]; then
        echo "[$(date)] FIREWALL OPEN" >> /tmp/poller.log
    fi
    sleep 0.05
done
