#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Skript zum Wiederherstellen einer Verbindung wenn diese nicht mehr aufgebaut ist
# nur fuer Python 2.x

import os
import time
import pycurl
import StringIO
import sys

router = "192.168.2.1" # Router mit VPN-Verbindungsdaten
hostname = "192.168.1.1" #Fritzbox @home
#response = os.system("ping -c 1 " + hostname)

#and then check the response...
def pingcheck():
   response = os.system("ping -c 1 " + hostname)
   if response == 0:
      print hostname, 'is up!'
      return True
   else:
      print hostname, 'is down!'
      return False

def post_data(data):
        encoded_data = ["Content-Type: text/xml", \
        "charset: utf-8", "SoapAction: urn:schemas-upnp-org:service:WANIPConnection:1#"+data]
        encoded_data2=("""<?xml version="1.0" encoding="utf-8"?>
        <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
        xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
        <s:Body>
        <u:"""+data+"""s xmlns:u="urn:schemas-upnp-org:service:WANIPConnection:1" />
        </s:Body>
        </s:Envelope>""")
        try:
                b = StringIO.StringIO()
                curl = pycurl.Curl()
                curl.setopt(pycurl.POSTFIELDS, encoded_data2)
                curl.setopt(pycurl.HTTPHEADER,encoded_data)
                curl.setopt(pycurl.TIMEOUT,10)
                curl.setopt(pycurl.CONNECTTIMEOUT,10)
                curl.setopt(pycurl.URL, "http://"+router+":49000/upnp/control/WANIPConn1")
                curl.setopt(pycurl.WRITEFUNCTION, b.write)
                curl.perform()
                return b.getvalue()
        except:
                print ("Error: connection problems.")
                exit(-1)
                 
def reconnect():
        # Start reconnect
        sys.stdout.write("Reconnect...")
        sys.stdout.flush()
        post_data("ForceTermination")
        print ("done.")


# Versuche 3 mal den Ping wenn nicht erfolgreich
counter = 0
bool = pingcheck()
while not bool and counter < 3:
   print hostname, "IP nicht erreichbar!"
   time.sleep(2)
   print "noch ein Versuch..."
   bool = pingcheck()
   counter = counter + 1

if counter >= 3:
   print "Fehler: 3 Versuche die Adresse ", hostname, " zu erreichen sind fehlgeschlagen!"
   print "Versuche eine Neuverbindung"
   reconnect()
   time.sleep(5)
   # hier kommt eine weiter pruefung und danach einer Weiterleitung per SMS
   exit(-1)
exit(0)
