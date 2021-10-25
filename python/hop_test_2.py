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
    
    """
    # first place, before anything
    print("before hop() elapsed time: --- %.2f seconds --- " % (float(time.time() - start_t)))
    dmtcp.hop2(src_ip, dst_ip, port)

    start_t3 = time.time()
    """

    if True:
        # get CrIS files 
        cris_geo_files = sorted(glob.glob(dataDir2+'SNDR.SNPP.CRIS*'))
        print ('cris_geo_files: ', cris_geo_files)
        # get VIIRS files 
        viirs_geo_files = sorted(glob.glob(dataDir4+'VNP03MOD*A*'+'*'))
        print ('viirs_geo_files: ', viirs_geo_files)

        # read VIIRS data 
        viirs_lon, viirs_lat, viirs_satAzimuth, viirs_satRange, viirs_satZenith, viirs_height, viirs_time = geo_QY.read_nasa_viirs_geo(viirs_geo_files)
        ### print ('viirs_time: ', viirs_time)
        ### print ('type(viirs_time): ', type(viirs_time))
        ### print ('viirs_time: ', viirs_time)
        print ('viirs_time.shape: ', viirs_time.shape)
        ### print ('viirs_time.min(): ', viirs_time.min())
        ### print ('viirs_time.max(): ', viirs_time.max())

        ### print ('viirs_lon: ', viirs_lon)
        ### print ('type(viirs_lon): ', type(viirs_lon))
        print ('viirs_lon.shape: ', viirs_lon.shape)

        start_time = viirs_time.min()
        end_time = viirs_time.max()

        # read CrIS data 
        cris_lon, cris_lat, cris_satAzimuth, cris_satRange, cris_satZenith, cris_time, cris_realLW = geo_QY.read_nasa_cris_geo(cris_geo_files)
        ### print ('cris_time: ', cris_time)
        print ('cris_time.min(): ', cris_time.min())
        print ('cris_time.max(): ', cris_time.max())

        if start_time < cris_time.min():
          start_time = cris_time.min()

        if end_time > cris_time.max():
          end_time = cris_time.max()

        print ('start_time: ', start_time)
        print ('end_time: ', end_time)

        """
        print('src_ip: ', src_ip)
        print('dst_ip: ', dst_ip)
        """

        # 2nd place, after input but before co-location
        print("*** before 1st hop() elapsed time: --- %.2f seconds --- " % (float(time.time() - start_t)))
        dmtcp.hop2(src_ip, dst_ip, port)

        print("*** after 1st hop() elapsed time: --- %.2f seconds --- " % (float(time.time() - start_t)))


print("started at: ", start_t)
print("now at: ", float(time.time()))
### print("------ at finish after 2nd hop() elapsed time --- %.2f seconds --- " % (float(time.time() - start_t3)))
print("*** total elapsed time: --- %.2f seconds --- " % (float(time.time() - start_t)))
print("done in --- %.2f seconds --- " % (float(time.time() - start_t)))

# collocation is done

