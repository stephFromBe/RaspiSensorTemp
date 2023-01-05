#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import fnmatch
import time
import MySQLdb as mdb
import logging

logging.basicConfig(filename='/home/pi/DS18B20_error.log',
  level=logging.DEBUG,
  format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger=logging.getLogger(__name__)

# Load the modules (not required if they are loaded at boot) 
# os.system('modprobe w1-gpio')
# os.system('modprobe w1-therm')

# Function for storing readings into MySQL
def insertDB( temperature,IDs):

  try:

    con = mdb.connect  (host="192.168.1.xx",user="user",passwd="pass",db="temperature", client_flag=131072,  use_unicode=True, charset="utf8", useSSL=False)  ;      # name of the data base
    
    cursor = con.cursor()

    for i in range(0,len(temperature)):
      sql = "INSERT INTO temperature(temperature,sensor_id) \
      VALUES ('%s', '%s')" % \
      ( temperature[i], IDs[i])
      cursor.execute(sql)
      sql = []
      con.commit()

    con.close()

 # except mdb.Error, e:
 #   logger.error(e)

# Get readings from sensors and store them in MySQL
  temperature = []
  IDs = []

for filename in os.listdir("/sys/bus/w1/devices"):
  if fnmatch.fnmatch(filename, '28-*'):
    with open("/sys/bus/w1/devices/" + filename + "/w1_slave") as f_obj:
      lines = f_obj.readlines()
      if lines[0].find("YES"):
        pok = lines[1].find('=')
        temperature.append(float(lines[1][pok+1:pok+6])/1000)
        IDs.append(filename)
      else:
        logger.error("Error reading sensor with ID: %s" % (filename))

if (len(temperature)>0):
  insertDB(temperature,IDs)
