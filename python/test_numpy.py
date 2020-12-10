import dmtcp
import numpy
a=numpy.array([0,1,2])
print('before checkpoint: ', a)
dmtcp.checkpoint()
print('after checkpoint: ', a)

# resuming after checkpoint, not restarting from checkpoint
if dmtcp.isResume():
  a=numpy.array([0,100,200])
  print('before restore: ', a)
  dmtcp.restore()  # this restarts from checkpoint

  # this will never be printed out
  # cause in case of resuming from checkpoint, the line above (restore) will cause restarting from checkpoint
  # otherwise in case of restarting from checkpoint, this entire if block will not be run at all
  print('after restore: ', a)  

