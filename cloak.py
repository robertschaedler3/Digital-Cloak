import getopt
import sys
import csv
import subprocess
import time


class Cloak():

  def __init__(self, ESSID_type, deauth_duration):
    # Devcie type to look for in a scan (eg: all ESSIDs that start with AA:BB:CC)
    self.essid_type = ESSID_type
    self.deauth_duration = deauth_duration
    # List to store all complete mac addresses that fit the ESSID_type
    self.results = []
    # Perform a network scan with airodump-ng and find all complete ESSIDs in the results that match the given ESSID_type
    self.scan()
    self.parseScan()
    self.cloak()
  
  def bash(self, command):
    """Runs a bash command in the terminal"""
    subprocess.call("{}".format(command), shell=True)
    

  def scan(self):
    """Scans all network traffic and stores the scan in a file"""
    self.bash("echo Enabling Monitor Mode")
    self.bash("airmon-ng start wlan0")
    self.bash("echo Scanning...")
    self.bash("airodump-ng -w scan --output-format csv wlan0mon")
    time.sleep(10)
    self.bash("killall airodump-ng")
      
        
  def parseScan(self):
    pass

  def cloak(self):
    pass

def main(argv):
  essid = ''
  duration = 10

  options, remainder = getopt.gnu_getopt(sys.argv[1:], 'he:d:', ['help', 'essid=', 'duration=' ])
  # print(options)
  for opt, arg in options:
    if opt in ('-h', '--help'):
      print()
      print ('cloak.py -e <ESSID> -d <duration>')
      print()
      sys.exit()
    elif opt in ('-e', '--essid'):
      essid = arg
    elif opt in ('-d', '--duration'):
      duration = arg
  Cloak(essid, duration)

if __name__ == "__main__":
  main(sys.argv[1:])