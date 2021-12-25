from multiprocessing import shared_memory, resource_tracker

name1 = 'test_smm'
### a = shared_memory.ShareableList(name=name1)
shm = shared_memory.SharedMemory(name='test_smm', size=10, create=False)
resource_tracker.unregister(shm._name, 'shared_memory')
print('shm: ', shm)
print('shm.buf: ', shm.buf)
print('shm.buf[2]: ', shm.buf[2])
shm.buf[2] += 1
### print('a._name: ', a._name)
### print('a: ', a)

### a.shm.close()

