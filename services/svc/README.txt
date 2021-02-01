. configure host.cfg
  cd git/navp/services/svc
  HOSTNAME = higgs.jpl.nasa.gov
  or
  HOSTNAME = weather.jpl.nasa.gov

. to start NAVP Bridging Services
  python3 run.py
  on both higgs and weather

. to demo loop_with_hop.py
  ssh higgs or weather
  cd /home/leipan/projects/dmtcp/git/navp/services/svc
  dmtcp_launch python /home/leipan/projects/dmtcp/git/navp/python/loop_with_hop.py

. to demo loop_with_hop.c

  # env var setup in .bashrc on higgs
  # dmtcp env vars
  export DMTCP_ROOT="/home/leipan/projects/dmtcp/git/3.0/dmtcp-master"
  export DEMO_PORT="7781"
  export LIBNAME="libdmtcp_plugin-to-announce-events"
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/leipan/projects/dmtcp/git/3.0/dmtcp-master/test/plugin/applic-initiated-ckpt

  . to build
    cd /home/leipan/projects/dmtcp/git/navp/c
    make -f make_loop_hop

  . to run
    cd /home/leipan/projects/dmtcp/git/navp/services/svc
    dmtcp_launch /home/leipan/projects/dmtcp/git/navp/c/loop_with_hop

. to call hop service
  curl "http://higgs.jpl.nasa.gov:8080/svc/hop?src_ip=137.78.248.95&dst_ip=137.78.73.87&port=6868&script=/home/leipan/projects/dmtcp/git/navp/services/svc/dmtcp_restart_script.sh"
