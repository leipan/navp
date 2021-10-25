import numpy as np
import glob
import geo_QY
import time
import pdb
import os, sys
import pickle
import shutil
import netCDF4 as nc4
from datetime import datetime
import dmtcp
import json
sys.path.append('/home/ops/navp/services/svc/svc/src/util')
from utils import get_host_port

# note:
# this script is run from navp/python/
# and the input/output are placed in /home/ops/matchup_pge/ in the docker container

def get_ips():

  protocol, hostname, port = get_host_port('/home/ops/navp/services/svc/host.cfg')
  print('port: ', port)

  ip2 = "127.0.0.1:28080"
  ip1 = "127.0.0.1:8080"

  if port in ip1:
    src_ip = ip1
    dst_ip = ip2
  else:
    src_ip = ip2
    dst_ip = ip1

  ### print('src_ip: ', src_ip)
  ### print('dst_ip: ', dst_ip)

  return src_ip, dst_ip
    
      
def swap_ips(src_ip, dst_ip):
  return dst_ip, src_ip



start_t = time.time()
print ('current dir: ', os.getcwd())

if not dmtcp.isEnabled:
  print('Run with dmtcp, like this: dmtcp_launch python %s'%__file__)
  sys.exit(-1)

src_ip, dst_ip = get_ips()
print('src_ip: ', src_ip)
print('dst_ip: ', dst_ip)
port = 7788

if True:
    # this script is run from navp/python/
    # and the input/output are placed in /home/ops/matchup_pge/ in the docker container
    dataDir2='/home/ops/matchup_pge/'
    dataDir4='/home/ops/matchup_pge/'
    
    # first place, before anything
    print("before hop() elapsed time: --- %.2f seconds --- " % (float(time.time() - start_t)))
    dmtcp.hop2(src_ip, dst_ip, port)

# datetime object containing current date and time
now = datetime.now()
print("now: ", now)

# dd/mm/YY H:M:S
dt_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")
print("date and time =", dt_string)	

print("started at: ", start_t)
print("now at: ", float(time.time()))
print("*** total elapsed time: --- %.2f seconds --- " % (float(time.time() - start_t)))

# collocation is done

