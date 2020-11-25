#!/usr/bin/env python
import shlex, subprocess
import os
import time
import sys

### command_line = input('What program to run: ')
command_line = sys.argv[1]

DMTCP_ROOT = os.environ.get('DMTCP_ROOT')
DEMO_PORT = os.environ.get('DEMO_PORT')

### dmtcp = DMTCP_ROOT+'/bin/dmtcp_launch --quiet --coord-port '+DEMO_PORT+' --with-plugin libdmtcp_plugin-to-announce-events.so '
dmtcp = DMTCP_ROOT+'/bin/dmtcp_launch --quiet --coord-port '+DEMO_PORT+' '
command_line = dmtcp + command_line

# run with dmtcp_launch
args = shlex.split(command_line)
print(args)
p = subprocess.Popen(args)
p.wait()

### time.sleep(10)

# run dmtcp_restart_script.sh
command_line = 'dmtcp_restart_script.sh --coord-host higgs.jpl.nasa.gov'
args = shlex.split(command_line)
print(args)
p = subprocess.Popen(args)
p.wait()

### time.sleep(10)

# run dmtcp_restart_script.sh
command_line = 'dmtcp_restart_script.sh --coord-host higgs.jpl.nasa.gov'
args = shlex.split(command_line)
print(args)
p = subprocess.Popen(args)
p.wait()

print('')
