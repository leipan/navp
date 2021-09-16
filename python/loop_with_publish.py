#!/usr/bin/env python

import dmtcp
import time
import sys
import socket
sys.path.append('/home/ops/navp/services/svc/svc/src/util')
from utils import get_host_port

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



if __name__ == '__main__':

  if not dmtcp.isEnabled:
    print('Run with dmtcp, like this: dmtcp_launch python %s'%__file__)
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
      dmtcp.publish(src_ip, dst_ip, port, 'ckpt')

      # swap the src and dst so we can hop back
      src_ip, dst_ip = swap_ips(src_ip, dst_ip)

  print('')

