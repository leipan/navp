#!/usr/bin/env python

import numpy as np
import dmtcp

x = 1
print ('before checkpoint() 1: ', x)

fdir = dmtcp.checkpointFilesDir()
print ('fdir: ', fdir)
fname = dmtcp.checkpointFilename()
print ('fname: ', fname)

dmtcp.checkpoint()
print ('after checkpoint() 1: ', x)









"""
x = 2
print ('before checkpoint() 2: ', x)
dmtcp.checkpoint()
print ('after checkpoint() 2: ', x)

x = 3
print ('before checkpoint() 3: ', x)
dmtcp.checkpoint()
print ('after checkpoint() 3: ', x)

"""
