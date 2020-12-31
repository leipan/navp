#!/usr/bin/env python
import os,sys

DMTCP_ROOT = os.getenv('DMTCP_ROOT')
print('DMTCP_ROOT: ', DMTCP_ROOT)
if DMTCP_ROOT != None:
  cmd = os.path.join(DMTCP_ROOT, 'bin/dmtcp_nocheckpoint')
  print('cmd: ', cmd)
else:
  sys.exit('Please set env variable: DMTCP_ROOT')
