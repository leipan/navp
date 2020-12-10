#!/usr/bin/env python

import os,sys
import time
import daemon
import signal
import lockfile
import boto3
import botocore
import json
import hashlib
from os.path import expanduser
from utils import usage_of_dir

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




def shutdown(signum, frame):  # signum and frame are mandatory

  sys.exit(0)




if __name__ == '__main__':

  cache_dirname = '/home/jpluser/m2020_crisp/imgreg_services/services/svc/svc/static/'

  # not a daemon
  """
  while True:
    purge_cache_dir(cache_dirname)
    time.sleep(1800) # kick of purging once every half an hour
  """

  ### home = expanduser("~")
  home = '/home/jpluser/'
  spam_pid = os.path.join(home, 'spam.pid')
  print ('spam_pid: ', spam_pid)

  # daemon
  # use: ps x|grep purging to get <pid> and kill -15 <pid> to send SIGTERM
  ### with daemon.DaemonContext(stdout=sys.stdout, stderr=sys.stderr,
  with daemon.DaemonContext(
    signal_map={signal.SIGTERM: shutdown, signal.SIGTSTP: shutdown},
                pidfile=lockfile.FileLock(spam_pid)):

    while True:
      purge_cache_dir(cache_dirname)
      time.sleep(1800) # kick of purging once every half an hour



