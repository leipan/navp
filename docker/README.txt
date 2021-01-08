. kill container
  docker ps
  docker kill 3a0eb412eb5f

. remove image
  docker images
  docker rmi --force a186f84c3981

. to build container
  docker build --rm -t dmtcp/dmtcp:latest .
  (--rm would allow reuse of the useful layers from the old one)

. to run dmtcp docker container
  docker run -ti <image>

. to get into a running container
  docker exec -u leipan -it <container ID> bash
