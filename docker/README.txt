. to clone from github
  git clone https://github.com/leipan/navp.git

. to remove an image
  docker images
  docker rmi --force a186f84c3981 (image ID)

. to build an image
  cd navp
  docker build --rm -t dmtcp/dmtcp:latest -f docker/matchup_Dockerfile .

. to run dmtcp docker container
  ### docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -ti dmtcp/dmtcp
  docker run --security-opt seccomp=unconfined -v /home/leipan/projects/aria_esi/wvcc/pge/data/collocation_output_1granule/test:/home/ops/data:rw -ti dmtcp/dmtcp /bin/bash
  (-v $host_dir:$guest_dir maps the host disk volume into the container)
  (place the 3 .nc files under $host_dir)

. to get into a running container (to run, e.g., dmtcp_command --checkpoint)
  docker ps (to get the <container ID>)
  docker exec -u 1000 -it <container ID> bash

. to debug the matchup/DMTCP integration
  cd data; strace -o tmp.log python ../CrIS_VIIRS_collocation-master/code_test_QY.py

  cd ; dmtcp_launch sh matchup_pge/run_matchup.sh
  (this leads to core dump)

  cd data; dmtcp_launch python ../CrIS_VIIRS_collocation-master/code_test_QY.py
  (this takes 39s)

  cd data; python ../CrIS_VIIRS_collocation-master/code_test_QY.py
  (this takes 16s)

-----------------------

. to run the matchup dmtcp docker container
  docker run -v /home/leipan/projects/aria_esi/wvcc/pge/data/collocation_output_1granule/test:/home/ops/data:rw -ti dmtcp/dmtcp /home/ops/matchup_pge/run_matchup.sh

. to run the scripts after getting into the container
  cd ~/navp/python/
  gdb --args python test_numpy.py
  (gdb) run

  or,
  gdb --args dmtcp_launch python test_numpy.py
  (gdb) run
  ^C
  (gdb) thread apply all bt

  or,
  gdb --args dmtcp_launch python test_KDTree.py
  (gdb) run
  ^C
  (gdb) thread apply all bt





