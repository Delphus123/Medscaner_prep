#!/bin/bash
cd /home/hal9000/Projects/preparo-exames
lsof -ti :5005 | xargs kill -9 2>/dev/null
sleep 1
nohup python3 server.py > server.log 2>&1 &
echo "Started: $!"
