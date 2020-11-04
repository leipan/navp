#!/usr/bin/env python

import dmtcp

print ('-------- 1 ----------')
x = 1
print ('before checkpoint() 1: ', x)
dmtcp.checkpoint()
print ('after checkpoint() 1: ', x)

print ('-------- 2 ----------')

x = 2
print ('before restore() 2: ', x)
dmtcp.restore()
print ('after restore() 2: ', x)

print ('-------- 3 ---------')

