#!/usr/bin/env python

import dmtcp
import time
import sys
import shlex, subprocess

def hop(src_ip, dst_ip, port):

  ### print("in hop.")
  dmtcp.checkpoint()
  time.sleep(1)
  ### print("checkpoint done.")


  if dmtcp.isResume():
    restart_cmd = \
      'curl "http://{0}:8080/svc/hop?src_ip={1}&dst_ip={2}&port={3}" 1>&2'.format(dst_ip, src_ip, dst_ip, port)
    print('restart_cmd: ', restart_cmd)

    args = shlex.split(restart_cmd)
    print(args)
    p = subprocess.Popen(args)
    p.wait()

    ### print("The process is resuming from a checkpoint.")
    # after hop(), the process will restart on a new node
    sys.exit(0)
  else:
    # restarting after hop() on a new node
    ### print("The process is restarting from a previous checkpoint.")
    pass
  return



if __name__ == '__main__':

  src_ip = "weather.jpl.nasa.gov"
  dst_ip = "higgs.jpl.nasa.gov"
  port = 7788

  l1 = 16
  n = 0
  while n < l1:
    print("%d " % (n), end="")
    sys.stdout.flush()
    time.sleep(1)

    if (n+1)%5 == 0:
      ### print("\n calling hop()")
      print("")
      port += 1
      hop(src_ip, dst_ip, port)

      ### swap the src and dst so we can hop back
      tmp = src_ip
      src_ip = dst_ip
      dst_ip = tmp

    n += 1
