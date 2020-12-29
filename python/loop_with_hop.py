#!/usr/bin/env python

import dmtcp
import time
import sys

def hop():

  ### print("in hop.")
  dmtcp.checkpoint()
  ### print("checkpoint done.")

  if dmtcp.isResume():
    ### print("The process is resuming from a checkpoint.")
    # after hop(), the process will restart on a new node
    sys.exit(0)
  else:
    # restarting after hop() on a new node
    ### print("The process is restarting from a previous checkpoint.")
    pass
  return



if __name__ == '__main__':

  l1 = 16
  n = 0
  while n < l1:
    print("%d " % (n), end="")
    sys.stdout.flush()
    time.sleep(1)

    if (n+1)%5 == 0:
      ### print("\n calling hop()")
      print("")
      hop()

    n += 1
