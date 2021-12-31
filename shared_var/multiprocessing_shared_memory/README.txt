. example 1
  host_shared_memory.py (host of shared mem)
  client_shared_memory.py (user of shared mem)

. example 2
  np_ndarray.py (host of np array)
  access_np_ndarray.py (user of np array)

. hop example
  on higgs, start two instances of the container
  docker run --security-opt seccomp=unconfined --network=host -v /home/leipan/projects/aria_esi/wvcc/pge/data/collocation_output_1granule/test:/home/ops/data:rw  -ti leipan/dmtcp:latest /bin/bash
  docker run --security-opt seccomp=unconfined --network=host -v /home/leipan/projects/aria_esi/wvcc/pge/data/collocation_output_1granule/test:/home/ops/data:rw  -ti leipan/dmtcp:latest /bin/bash

  get into one container in two other windows
  docker exec -u ops -it <container ID> bash
  docker exec -u ops -it <container ID> bash

  change in one container the port number in
  settings.cfg, host.cfg under /home/ops/navp/services/svc
  from 8080 to 28080

  run
  python run.py
  under /home/ops/navp/services/svc
  in both containers

  in one container
  under /home/ops/navp/shared_var/multiprocessing_shared_memory
  run
  python np_ndarray.py
  in one window, and
  dmtcp_launch python hop_np_ndarray.py
  in another

  error seen:
  ----------
  command_line:  sh ./dmtcp_restart_script.sh --coord-port 7788 --coord-host localhost
  ['sh', './dmtcp_restart_script.sh', '--coord-port', '7788', '--coord-host', 'localhost']
  [363] ERROR at coordinatorapi.cpp:569 in sendRecvHandshake; REASON='JASSERT(false) failed'
       *compId = 7ebac2d2d3962be3-40000-3b9cae3b2ce475
  Message: Connection rejected by the coordinator.
   Reason: This process has a different computation group.
  dmtcp_restart (363): Terminating...
  

