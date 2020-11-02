. to build container
  docker build --rm -t dmtcp/dmtcp:latest .
  (--rm would allow reuse of the useful layers from the old one)

. to run dmtcp docker container
  docker run -ti <image>
  docker-compose up -d

. to get into a running container
  docker exec -u leipan -it <container ID> bash
