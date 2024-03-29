#!/usr/bin/env python

import os
import sys
import time
import glob
import logging
import ctypes
import re
logger = logging.getLogger(__name__)


# find the ckpt file pointed at by dmtcp_restart_script.sh
def parse_script(script):

  file1 = open(script, 'r')
  Lines = file1.readlines()

  for line in Lines:
    if 'given_ckpt_files=' in line:
      ### print("line: {}".format(line.strip()))
      var = re.findall(r'([\w]+)=', line.strip())
      ### print("var: {}".format(var))
      value = re.findall(r'=([\w\.\-\/\_\ \"]+)', line.strip())
      ### print("value: {}".format(value))

  file1.close()

  print('value[0]: ', value[0])
  ### value1 = value[0].replace('"', '')
  value1 = value[0].strip() # get rid of leading and trailing whitespaces
  value1 = value1.replace('"', '')
  value1 = value1.split()
  return value1



def get_host_port(cfg_file):

    myvars = {}

    try:
      myvars["HOSTNAME"] = os.environ['DOMAIN']
      myvars["PORT"] = os.environ['PORT']

      ### myvars["REDIS_ENDPOIT"] = os.environ['REDIS_ENDPOIT']
      ### myvars["REDIS_PORT"] = os.environ['REDIS_PORT']
      ### myvars["REDIS_USERNAME"] = os.environ['REDIS_USERNAME']
      ### myvars["REDIS_PASSWORD"] = os.environ['REDIS_PASSWORD']

      protocol = 'http'
    except KeyError:
      myfile =  open(cfg_file)
      for line in myfile:
        if not line.startswith('#'):
          name, var = line.partition("=")[::2]
          name = name.strip()
          var = var.strip('\n').strip()
          if name is not '' and var is not '':
            myvars[name] = var

      protocol = 'http'

    return protocol, myvars["HOSTNAME"], myvars["PORT"]


def usage_of_dir(dirname):

  st = os.statvfs(dirname)
  ### print ('st: {}'.format(st))

  return (100. - st.f_bavail*100./st.f_blocks)



def get_ips():
  ### ip1 = "weather2.jpl.nasa.gov"
  ### ip2 = "higgs.jpl.nasa.gov"

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


def age_of_file(filepath):

  x=os.stat(filepath)
  age = (time.time() - x.st_mtime) 
  print ("The age of the given file is: ", age)

  return age


# start purging when usage is above 70%
# 604800 seconds is a week, which is the initial max_age
# if in a round the goal of cutting down to below a 70% usage is not achieved, a new round is started
# for which we cut the max_age by half
# if in a round no file can be removed, terminate the entire purging
def purge_cache_dir(cache_dir, exts=['*.VIC', '*.IMG', '*.png'], max_age=604800, usage_threshold=70):

  age = 2*max_age
  print ('age: {0}'.format(age))
  usage = usage_of_dir(cache_dir)
  print ('usage: {0}'.format(usage))

  # for testing
  ### usage_threshold = 30

  # purge as long as usage is above threshold
  while usage > usage_threshold:
    age /= 2.0  # for a new round, remove files that are less old
    num_files_deleted = 0
    for ext in exts:  # only remove files with certain extensions
      pattern = os.path.join(cache_dir, ext)
      ### print ('pattern: {0}'.format(pattern))
      list1 = glob.glob(pattern)
      ### print ('list1: {}'.format(list1))
      for file1 in list1:
        age1 = age_of_file(file1)
        if age1 > age: # remove files older than age
          print ('deleting file: {}'.format(file1))
          os.remove(file1)
          num_files_deleted += 1

    # if no more room is made in this round
    # no need to run the while loop further
    if num_files_deleted == 0:
      break
    usage = usage_of_dir(cache_dir) # get new usage after this round
    print ('usage: {0}'.format(usage))




if __name__ == '__main__':

  dirname = '/home/jpluser/github/CRISP_docker/docker/m2020_crisp/imgreg_services/services/svc/svc/static/'
  usage = usage_of_dir(dirname)
  logger.info('usage: {0}'.format(usage))
  print ('usage: {0}'.format(usage))

  age = age_of_file(os.path.join(dirname, 'ICM-FRB_517245225ILT_F0541490FHAZ00323M1-NLB_517175096ILT_F0541490NCAM00207M1-J01.VIC'))
  logger.info('age: {0}'.format(age))
  ### print ('age: {0}'.format(age))

  ### purge_cache_dir('/home/jpluser/tmp/cache')
  dirname2 = '/home/jpluser/m2020_crisp/imgreg_services/services/svc/svc/static'
  purge_cache_dir(dirname2)

  ### remember to delete the public dir, and use cache dir name for scratch space


