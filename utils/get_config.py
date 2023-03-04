import configparser
import sys

config = configparser.ConfigParser()
try:
  config.read(sys.argv[1] or 'conf.ini')
except:
  config.read('conf.ini')

def GetConfig():
  for i in config:
    for t in i:
      t = str(t)
  return config