# my own domotic project based on raspberrypi+mqtt

## installation
### raspberrypi
assume that you have installed a fresh raspbian…

### mqtt
sudo apt-get install mosquitto mosquitto-clients python-mosquitto

## sensors (mosquitto_pub)
several sensors push data over mqtt (read crontab.txt)
- pi temperature
- home int. temperature (via CurrentCost ENVI cc128, and via ws => https://github.com/lalelunet/measureit)
- power consumption (via CurrentCost ENVI cc128, and via ws => https://github.com/lalelunet/measureit)
- home ext. temperature and wind (via yahoo weather webservice)
- via bluetooth LE usb dongle (later?)

## analyzers (mosquitto_sub)
several analyzers are available
- push data to syslog
- push data to csv
- push data to graphite
- push data to thinkspeak
