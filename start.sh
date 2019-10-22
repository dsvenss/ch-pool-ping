#!/bin/bash
echo "Starting pool-ping"
cd /home/pi/projects/ch-pool-ping/src && python3 main.py > /home/pi/pool-ping.log 2>&1 &
exit 0