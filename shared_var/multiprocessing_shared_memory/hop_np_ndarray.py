import sys,os,time
import numpy as np
from multiprocessing import shared_memory, resource_tracker
sys.path.append('/home/ops/navp/services/svc/svc/src/util')
from utils import get_host_port, get_ips, swap_ips
sys.path.append('/home/ops/navp/python')
import dmtcp

# note:
# this script is run from navp/shared_var/multiprocessing_shared_memory
# and the input/output are placed in /home/ops/data/ in the docker container

start_t = time.time()
print ('current dir: ', os.getcwd())

if not dmtcp.isEnabled:
  print('Run with dmtcp, like this: dmtcp_launch python %s'%__file__)
  sys.exit(-1)

src_ip, dst_ip = get_ips()
print('src_ip: ', src_ip)
print('dst_ip: ', dst_ip)
port = 7788


d_shape = (10,)
d_type = np.int64
shm_name = 'test_shm_np'

try:
  # In other processes
  # reuse existing shared memory
  ex_shm = shared_memory.SharedMemory(name=shm_name, create=False)
  resource_tracker.unregister(ex_shm._name, 'shared_memory')
  # numpy array on existing memory buffer, a and b read/write the same memory
  b = np.ndarray(shape=d_shape, dtype=d_type, buffer=ex_shm.buf)
  print('len(b): ', len(b))
  print('b[1]: ', b[1])
  b[1] += 1
  print('b: ', b)

  ex_shm.close()  # close after using

  # test if the shared memory is checkpointed and brought with hop2()
  dmtcp.hop2(src_ip, dst_ip, port)

  print("started at: ", start_t)
  print("now at: ", float(time.time()))
  print("*** total elapsed time: --- %.2f seconds --- " % (float(time.time() - start_t)))

except FileNotFoundError:
  print('Error: shared memory {} does not exist'.format(shm_name))
