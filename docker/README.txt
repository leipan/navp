. to clone from github
  git clone https://github.com/leipan/navp.git

. to remove an image
  docker images
  docker rmi --force a186f84c3981 (image ID)

. to build an image
  cd navp
  ### docker build --rm -t dmtcp/dmtcp:latest -f docker/matchup_Dockerfile .
  docker build --rm -t leipan/dmtcp:latest -f docker/matchup_Dockerfile .

. to push the image to dockerhub
  docker login
  docker push leipan/dmtcp:latest

. to run dmtcp docker container
  ### docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -ti dmtcp/dmtcp
  docker run --security-opt seccomp=unconfined --network=host -v /home/leipan/projects/aria_esi/wvcc/pge/data/collocation_output_1granule/test:/home/ops/data:rw -ti dmtcp/dmtcp /bin/bash

  docker run --security-opt seccomp=unconfined --network=host -v /home/leipan/projects/aria_esi/wvcc/pge/data/collocation_output_1granule/test2:/home/ops/data:rw -ti leipan/dmtcp:latest /bin/bash

  (-v $host_dir:$guest_dir maps the host disk volume into the container)

  (place the 4 .nc files under $host_dir)

. will use two navp bridging services:
  . one deployed to 127.0.0.1:8080 running inside a container
  . one deployed to 127.0.0.1:28080 running inside another container
  . their /home/ops/data dirs are bound to the same dir on the host

. to get into a running container (to run, e.g., dmtcp_command --checkpoint)
  docker ps (to get the <container ID>)
  ### docker exec -u 1000 -it <container ID> bash
  docker exec -u ops -it <container ID> bash

. to copy all the files/dirs under a dir (e.g., /home/leipan/tmp/)
  into a container:
  docker cp /home/leipan/tmp/. a8d9790b205d:/home/ops/tmp

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





