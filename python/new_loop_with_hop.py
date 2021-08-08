#!/usr/bin/env python

import dmtcp
import time
import sys
import socket

def get_ips():
  ### ip1 = "weather2.jpl.nasa.gov"
  ### ip2 = "higgs.jpl.nasa.gov"

  ip1 = "127.0.0.1:18080"
  ip2 = "127.0.0.1:8080"

  ### src_ip = socket.gethostname()
  src_ip = ip1

  dst_ip = ip2
  if dst_ip == src_ip:
    dst_ip = ip1

  return src_ip, dst_ip


def swap_ips(src_ip, dst_ip):
  return dst_ip, src_ip



if __name__ == '__main__':

  if not dmtcp.isEnabled:
    print('Run with dmtcp, like this: dmtcp_launch python loop_with_hop.py')
    sys.exit(-1)

  src_ip, dst_ip = get_ips()
  print('src_ip: ', src_ip)
  print('dst_ip: ', dst_ip)
  port = 7788

  loop_bound = 20

  for i in range(loop_bound):
    print("%d " % (i), end="")
    sys.stdout.flush()
    time.sleep(1)

    if (i+1)%5 == 0:
      print("")
      port += 1
      dmtcp.hop(src_ip, dst_ip, port)

      # swap the src and dst so we can hop back
      src_ip, dst_ip = swap_ips(src_ip, dst_ip)

  print('')

