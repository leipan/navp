#!/usr/bin/env python

import os
import sys
import time
import glob
import logging
logger = logging.getLogger(__name__)

import ctypes

def get_host_port(cfg_file):

    myvars = {}

    try:
      myvars["HOSTNAME"] = os.environ['DOMAIN']
      myvars["PORT"] = os.environ['PORT']

      ### myvars["REDIS_ENDPOIT"] = os.environ['REDIS_ENDPOIT']
      ### myvars["REDIS_PORT"] = os.environ['REDIS_PORT']
      ### myvars["REDIS_USERNAME"] = os.environ['REDIS_USERNAME']
      ### myvars["REDIS_PASSWORD"] = os.environ['REDIS_PASSWORD']

      protocol = 'https'
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

"""
      - PORT=:443
      - NEO4J_ENDPOIT=100.64.49.54
      - NEO4J_PORT=7687
      - NEO4J_USERNAME=neo4j
      - NEO4J_PASSWORD=m2020
      - MARIADB_ENDPOIT=100.64.49.54
      - MARIADB_PORT=3306
      - MARIADB_USERNAME=root
      - MARIADB_PASSWORD=m2020
"""


def usage_of_dir(dirname):

  st = os.statvfs(dirname)
  ### print ('st: {}'.format(st))

  return (100. - st.f_bavail*100./st.f_blocks)


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


