. to clone from github
  git clone https://github.com/leipan/navp.git

. to remove an image
  docker images
  docker rmi --force a186f84c3981 (image ID)

. to build an image
  cd navp/docker (where Dockerfile is)
  docker build --rm -t dmtcp/dmtcp:latest .

. to run dmtcp docker container
  docker run --cap-add=SYS_PTRACE --security-opt seccomp=unconfined -ti dmtcp/dmtcp

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
