from multiprocessing import shared_memory

a = shared_memory.ShareableList(name='psm_eb6c619a')
print('a: ', a)

a.shm.close()
del a
