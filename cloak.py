import getopt
import sys
import csv
import subprocess
from threading import Timer
import time


class Cloak():

  def __init__(self, ESSID_type, deauth_duration):
    # Devcie type to look for in a scan (eg: all ESSIDs that start with AA:BB:CC)
    self.essid_type = ESSID_type
    self.deauth_duration = deauth_duration
    # List to store all complete mac addresses that fit the ESSID_type
    self.results = []
    # Perform a network scan with airodump-ng and find all complete ESSIDs in the results that match the given ESSID_type
    self.kill = lambda process: process.kill()
    self.scan()
    self.parseScan()
    self.cloak()
  
  def bash(self, command, terminates=True, timeout=30):
    """Runs a bash command in the terminal"""
    if terminates:
      subprocess.call("{}".format(command), shell=True)
    else:
      process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      timer = Timer(30, self.kill, process)
      try:
        timer.start()
        stdout, stderr = process.communicate()
      finally:
        timer.cancel()


    

  def scan(self):
    """Scans all network traffic and stores the scan in a file"""
    self.bash("echo Enabling Monitor Mode")
    self.bash("airmon-ng start wlan0")
    self.bash("echo Scanning...")
    self.bash("airodump-ng -w scan --output-format csv wlan0mon")
    time.sleep(10)
    self.bash("killall airodump-ng")
         
  def parseScan(self):
    """Function that opens the output file from the the scan and parses the data"""
    pass

  def cloak(self):
    """Preforms the cloaking function by deauthing all devices that matched the given ESSID type"""
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