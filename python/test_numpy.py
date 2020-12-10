import dmtcp
import numpy
a=numpy.array([0,1,2])
print('before checkpoint: ', a)
dmtcp.checkpoint()
print('after checkpoint: ', a)
a=numpy.array([0,100,200])
print('before restore: ', a)
dmtcp.restore()
print('after restore: ', a)

