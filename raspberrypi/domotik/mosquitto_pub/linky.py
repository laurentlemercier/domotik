#!/usr/bin/python
import paho.mqtt.client as mqtt
import argparse
import serial
import sys
import errno
import re
import signal
import os

parser = argparse.ArgumentParser(description='fetch data from linky and push it to mqtt')
parser.add_argument('usbport', metavar='usbport', help='usb port like /dev/serial0', nargs='?', default='/dev/serial0')
parser.add_argument('hostname', metavar='hostname', help='hostname of mqtt server', nargs='?', default="0.0.0.0")
parser.add_argument('port', metavar='port', help='port of mqtt server', nargs='?', default="1883")
args = parser.parse_args()

usbport = args.usbport
run = True

def lectureTrame(ser):
    """Lecture d'une trame sur le port serie specifie en entree.
    La trame debute par le caractere STX (002 h) et fini par ETX (003 h)"""
    # Lecture d'eventuel caractere avant le debut de trame
    # Jusqu'au caractere \x02 + \n (= \x0a)
    trame = list()
    while trame[-2:]!=['\x02','\n']:
        trame.append(ser.read(1))
    # Lecture de la trame jusqu'au caractere \x03
    trame=list()
    while trame[-1:]!=['\x03']:
        trame.append(ser.read(1))
    # Suppression des caracteres de fin '\x03' et '\r' de la liste
    trame.pop()
    trame.pop()
    return trame

def decodeTrame(trame):
    """Decode une trame complete et renvoie un dictionnaire des elements"""
    lignes = trame.split('\r\n')
    result = {}
    for ligne in lignes:
        tuple = valideLigne(ligne)
        result[tuple[0]]=tuple[1]
    return result

def valideLigne(ligne):
    """Retourne les elements d'une ligne sous forme de tuple si le checksum est ok"""
    chk = checksumLigne(ligne)
    items = ligne.split(' ')
    if ligne[-1]==chk:
        return (items[0], items[1])
    else:
        raise Exception("Checksum error")

def checksumLigne(ligne):
    """Verifie le checksum d'une ligne et retourne un tuple"""
    sum = 0
    for ch in ligne[:-2]:
            sum += ord(ch)
    sum = (sum & 63) + 32
    return chr(sum)

def signal_handler(signal, frame):
    global run
    print "Ending and cleaning up"
    ser.close()
    client.disconnect()
    run = False

try:
    print("Starting listening Linky")
    signal.signal(signal.SIGINT, signal_handler)

    while not os.path.exists(usbport):
        print "waiting for", usbport
        time.sleep(2)

    ser = serial.Serial(port=usbport, baudrate=1200, bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
    client = mqtt.Client()
    client.connect(args.hostname, int(args.port), 60)
except Exception as e:
    print e
    sys.exit(errno.EIO)

while run:
    try:
        client.loop()
        trame = lectureTrame(ser)
        lignes = decodeTrame("".join(trame))
        client.publish("sensors/linky/watt", lignes["PAPP"])
    except:
        sys.exit(errno.EIO)
