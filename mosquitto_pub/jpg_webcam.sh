#!/bin/bash
CAPTURE=/tmp/capture.jpg
$HOME/domotik/services/service-captureCamera.sh $CAPTURE
base64 -w 0 $CAPTURE | mosquitto_pub -t sensors/camera/jpg -s
