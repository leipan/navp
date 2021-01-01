#!/usr/bin/env python

import dmtcp
import time
import sys
import socket

if __name__ == '__main__':

  ip1 = "weather2.jpl.nasa.gov"
  ip2 = "higgs.jpl.nasa.gov"

  src_ip = socket.gethostname()
  dst_ip = ip2
  if dst_ip == src_ip:
    dst_ip = ip1

  print('src_ip: ', src_ip)
  print('dst_ip: ', dst_ip)

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
      dmtcp.hop(src_ip, dst_ip, port)

      ### swap the src and dst so we can hop back
      tmp = src_ip
      src_ip = dst_ip
      dst_ip = tmp

    n += 1

  print('')

