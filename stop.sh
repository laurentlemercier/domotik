#!/bin/bash
echo "stopping mosquitto subscribing..."
killall mosquitto_sub
sudo killall /usr/bin/python
echo "stopping web interface..."
cd $HOME/domotik/web
npm stop
echo "bye"
