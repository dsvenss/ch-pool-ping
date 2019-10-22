#!/bin/bash
echo "Starting pool-ping"
cd /home/pi/projects/ch-pool-ping && git pull && cd src && python3 main.py > /home/pi/pool-ping.log 2>&1 &
echo "Started pool-ping"
exit 0
