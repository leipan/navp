#!/usr/bin/env python

# The contents of this file are inspired from the python script dmtcp_ctypes.py
# originally supplied by Neal Becker.

import os,sys
import glob
import subprocess
from ctypes import *
import subprocess
import time
import shlex
import shutil
import requests
from datetime import datetime
sys.path.append('/home/ops/navp/services/svc/svc/src/util')
from utils import parse_script

ckptRetVal = 0
sessionList = []
vncserver_addr = -1

libdmtcp = CDLL(None)
try:
    isEnabled         = libdmtcp.dmtcp_is_enabled;
    checkpoint        = libdmtcp.dmtcp_checkpoint;
    disableCkpt       = libdmtcp.dmtcp_disable_ckpt;
    enableCkpt        = libdmtcp.dmtcp_enable_ckpt;

    getCkptFilename   = libdmtcp.dmtcp_get_ckpt_filename
    getCkptFilename.restype = c_char_p

    getUniquePidStr   = libdmtcp.dmtcp_get_uniquepid_str;
    getUniquePidStr.restype = c_char_p

except AttributeError:
    isEnabled = False;

def numProcesses():
    n = c_int(-1)
    ir = c_int(0)
    if isEnabled:
        libdmtcp.dmtcp_get_coordinator_status(byref(n), byref(ir))
    return n.value

def isRunning():
    n = c_int()
    ir = c_int(0)
    if isEnabled:
        libdmtcp.dmtcp_get_coordinator_status(byref(n), byref(ir))
    return ir.value == 1


def numCheckpoints():
    numCkpt = c_int()
    numRst = c_int()
    if isEnabled:
        libdmtcp.dmtcp_get_local_status(byref(numCkpt), byref(numRst))
    return numCkpt.value

def numRestarts():
    numCkpt = c_int()
    numRst = c_int()
    if isEnabled:
        libdmtcp.dmtcp_get_local_status(byref(numCkpt), byref(numRst))
    return numRst.value

def checkpointFilename():
    if isEnabled:
        ### return getCkptFilename()
        return getCkptFilename().decode("utf-8")
    return ""

def checkpointFilesDir():
    if isEnabled:
        ### return getCkptFilename().replace('.dmtcp', '_files')
        return getCkptFilename().decode("utf-8").replace('.dmtcp', '_files')
    return ""

def uniquePidStr():
    if isEnabled:
        return getUniquePidStr()
    return ""

def checkpoint():
    global ckptRetVal
    if isEnabled:
        ckptRetVal = libdmtcp.dmtcp_checkpoint()
    # sessionId = libdmtcp.dmtcpCheckpoint()

def isResume():
    global ckptRetVal
    return ckptRetVal == 1

def isRestart():
    global ckptRetVal
    return ckptRetVal == 2

def restore(sessionId = 0):
    if sessionId == 0:
        if len(sessionList) == 0:
            createSessionList()
        if len(sessionList) == 0:
            print('No checkpoint session found')
            return
        print('Restoring the latest session')
    else:
        if len(sessionList) == 0:
            print('Please do a listSession to see the list of available sessions')
            return
        if sessionId < 1 or sessionId > len(sessionList):
            return 'Invalid session id'

    ### print ('sessionId: ', sessionId)
    session = sessionList[sessionId - 1]
    ### print ('session: ', session)
    print ('session[1]: ', os.path.realpath(session[1]))

    # in order to run the shell script under the current dir using os.execlp()
    # the current dir '.' must be included in PATH (set in ~/.bashrc)

    # the higgs/weather intallation location
    ### os.execlp('/home/leipan/local/dmtcp_installation/bin/dmtcp_nocheckpoint', 'sh', os.path.realpath(session[1]))
    # the pleiades installation location
    ### os.execlp('/home1/lpan/local/dmtcp3_0/bin/dmtcp_nocheckpoint', 'sh', os.path.realpath(session[1]))

    DMTCP_ROOT = os.getenv('DMTCP_ROOT')
    ### print('DMTCP_ROOT: ', DMTCP_ROOT)
    if DMTCP_ROOT != None:
      cmd = os.path.join(DMTCP_ROOT, 'bin/dmtcp_nocheckpoint')
      print('cmd: ', cmd)
      os.execlp(os.path.join(DMTCP_ROOT, 'bin/dmtcp_nocheckpoint'), 'sh', os.path.realpath(session[1]))
    else:
      sys.exit('Please set env variable: DMTCP_ROOT')


def hop(src_ip, dst_ip, port):

  ### print("in hop.")
  ### dmtcp.checkpoint()
  checkpoint()
  time.sleep(1)
  ### print("checkpoint done.")

  ### fname = dmtcp.checkpointFilename()
  fname = checkpointFilename()
  if fname != '':
    print ('fname: ', fname)

  ### if dmtcp.isResume():
  if isResume():
    restart_cmd = \
      'curl "http://{0}/svc/hop?src_ip={1}&dst_ip={2}&port={3}&ckpt={4}" '.format(dst_ip, src_ip, dst_ip, port, fname)
    ### print('restart_cmd: ', restart_cmd)

    args = shlex.split(restart_cmd)
    ### print(args)
    p = subprocess.Popen(args)
    p.wait()

    ### print("The process is resuming from a checkpoint.")
    # after hop(), the process will restart on a new node
    sys.exit(0)
  else:
    # restarting after hop() on a new node
    ### print("The process is restarting from a previous checkpoint.")
    pass
  return




def restart(src_ip, dst_ip, port, job_id):
  # get dmtcp_restart_script.sh from /home/ops/data/<id>
  restart_script = 'dmtcp_restart_script.sh'
  script_path = os.path.join('/home/ops/data', job_id, restart_script)

  # parse dmtcp_restart_script.sh to get the full path of dmtcp files
  parsed_ckpt_files = parse_script(script_path)

  # copy the dmtcp files to where they belong
  for ckpt_file in parsed_ckpt_files:
    src_dir = os.path.join('/home/ops/data', job_id)
    base_name = os.path.basename(ckpt_file)
    src_path = os.path.join(src_dir, base_name)

    print('src_path: ', src_path)
    print('ckpt_file: ', ckpt_file)
    shutil.copyfile(src_path, ckpt_file)
    print('copied {0} to {1}'.format(src_path, ckpt_file))
    os.remove(src_path)
    print('removed {0}'.format(src_path))

    # run dmtcp_restart_script.sh
    ### command_line = 'sh ' + script_path + ' --coord-port ' + str(int(port)+30) + ' --coord-host localhost'
    command_line = 'sh ' + script_path
    args = shlex.split(command_line)
    print(args)
    p = subprocess.Popen(args)
    p.wait()

    # print out subprocess output
    out, err = p.communicate()
    print('out: ', out)
    print('err: ', err)

    # remove dmtcp files
    if os.path.exists(script_path):
      os.remove(script_path)
    if os.path.exists(src_path):
      os.remove(src_path)
    if os.path.exists(ckpt_file):
      os.remove(ckpt_file)



def publish(src_ip, dst_ip, port, status, job_id):

  print("in publish, src_ip: {0}, dst_ip: {1} with status={2}".format(src_ip, dst_ip, status))

  if status == 'ckpt':
    # checkpoint
    checkpoint()
    time.sleep(1)

    if isResume():

      fname = checkpointFilename()
      if fname != '':
        print ('fname: ', fname)
        ckpt_basename = os.path.basename(fname)
        prefix = fname.replace(ckpt_basename, '')
        print('prefix: ', prefix)

        # copy dmtcp files to a subdir named by time
        ### time_string = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        ### subdir1 = os.path.join('/home/ops/data/', time_string)
        subdir1 = os.path.join('/home/ops/data/', job_id)
        print('subdir1: ', subdir1)

        if os.path.isdir(subdir1):
          shutil.rmtree(subdir1)

        if not os.path.isdir(subdir1):
          os.mkdir(subdir1)

        """ parse the restart script first, and then copy the ckpt files (below)
        shutil.copyfile(fname, os.path.join(subdir1, ckpt_basename))
        print('copied {0} to {1}'.format(fname, os.path.join(subdir1, ckpt_basename)))
        os.remove(fname)
        print('removed {0}'.format(fname))
        """

        real_script = os.path.realpath('./dmtcp_restart_script.sh')
        print('real_script: ', real_script)
        shutil.copyfile(real_script, os.path.join(subdir1, 'dmtcp_restart_script.sh'))
        print('copied {0} to {1}/dmtcp_restart_script.sh'.format(real_script, subdir1))
        if os.path.exists('./dmtcp_restart_script.sh'):
          os.remove('./dmtcp_restart_script.sh')
          print('removed {0}'.format('./dmtcp_restart_script.sh'))
          os.remove(real_script)
          print('removed {0}'.format(real_script))

        parsed_ckpt_files = parse_script(os.path.join(subdir1, 'dmtcp_restart_script.sh'))
        print('parsed_ckpt_files parsed: ', parsed_ckpt_files)

        for ckpt_file in parsed_ckpt_files:
          ckpt_file_basename = os.path.basename(ckpt_file)
          shutil.copyfile(ckpt_file, os.path.join(subdir1, ckpt_file_basename))
          print('copied {0} to {1}'.format(ckpt_file, os.path.join(subdir1, ckpt_file_basename)))
          os.remove(ckpt_file)
          print('removed {0}'.format(ckpt_file))

        cmd = 'http://{0}/svc/publish_job?status={1}&id={2}'.format(dst_ip, 'ckpt', job_id)
        print('cmd: ', cmd)

        x = requests.get(cmd)
        print(x.text)

        ### sys.exit(0)

      # call service publish_job with status and subdir name

      # continue running the app
  elif status == 'finished':

    # call service publish_job with status='finished' and subdir name
    restart_cmd = 'http://{0}/svc/publish_job?status={1}&id={2}'.format(dst_ip, 'finished', job_id)
    print('restart_cmd: ', restart_cmd)

    x = requests.get(restart_cmd)
    print(x.text)

    # remove the dmtcp files if there
    for file1 in glob.glob(os.path.join('/home/ops/data/', str(job_id), '*')):
      ### print('file1: ', file1)
      if 'dmtcp_' in file1 and '.sh' in file1:
        parsed_ckpt_files = parse_script(file1)

        for ckpt_file in parsed_ckpt_files:
          print('ckpt_file: ', ckpt_file)
          ### if os.path.exists(ckpt_file):
          if os.path.isfile(ckpt_file):
            os.remove(ckpt_file)
            print('removed {0}'.format(ckpt_file))

        os.remove(file1)
        print('dmtcp restart shell script: {} removed'.format(file1))

      if 'ckpt_' in file1 and '.dmtcp' in file1:
        os.remove(file1)
        print('dmtcp file: {} removed'.format(file1))


# end of publish()





def hop2(src_ip, dst_ip, port):

  executionStartTime = int(time.time())

  print("in hop, from {0} to {1}".format(src_ip, dst_ip))
  ### dmtcp.checkpoint()

  executionStartTime2 = int(time.time())
  checkpoint()
  executionEndTime2 = float(time.time())

  time.sleep(1)
  ### print("checkpoint done.")

  fname = checkpointFilename()
  if fname != '':
    print ('fname: ', fname)

  if isResume():

    print ('****** checkpoint() (in hop2()) elapsed time: ', executionEndTime2 - executionStartTime2)

    # copy fname and dmtcp_restart_script.sh to ~/data mount if it is not there yet
    # in the future we could use AWS s3 buckets
    prefix = ''
    if fname != '':
      ckpt_basename = os.path.basename(fname)
      prefix = fname.replace(ckpt_basename, '')
      print('prefix: ', prefix)

      if prefix != '':
        if prefix != '/home/ops/data/':
          shutil.copyfile(fname, os.path.join('/home/ops/data/', ckpt_basename))
          print('copied {} to /home/ops/data/'.format(fname))
          os.remove(fname)
          print('removed {0}'.format(fname))

        real_script = os.path.realpath('./dmtcp_restart_script.sh')
        print('real_script: ', real_script)
        shutil.copyfile(real_script, os.path.join('/home/ops/data/', 'dmtcp_restart_script.sh'))
        print('copied {} to /home/ops/data/dmtcp_restart_script.sh'.format(real_script))
        os.remove(real_script)
        print('removed {0}'.format(real_script))

        # call service hop2()
        ### restart_cmd = 'curl "http://{0}/svc/hop2?port={1}&ckpt={2}" '.format(dst_ip, port, ckpt_basename)
        restart_cmd = 'http://{0}/svc/hop2?port={1}&ckpt={2}'.format(dst_ip, port, ckpt_basename)
        print('restart_cmd: ', restart_cmd)

        """
        args = shlex.split(restart_cmd)
        print('args: ', args)
        p = subprocess.Popen(args)
        p.wait()
        """

        x = requests.get(restart_cmd)
        print(x.text)

    ### print("The process is resuming from a checkpoint.")
    # after hop(), the process will restart on a new node

    executionEndTime = float(time.time())
    print ('****** hop() elapsed time: ', executionEndTime - executionStartTime)

    sys.exit(0)
  else:
    # restarting after hop() on a new node
    ### print("The process is restarting from a previous checkpoint.")
    pass
  return



def createSessionList():
    global sessionList
    restartScripts = glob.glob('dmtcp_restart_script_*.sh')
    for script in restartScripts:
        for line in open(script):
            if 'ckpt_timestamp' in line:
                tstamp = line.split('"')[1]
                sessionList = [(tstamp, script)] + sessionList
                break;
    sessionList.sort()

def listSessions():
    global sessionList
    if len(sessionList) == 0:
        createSessionList()
    count = 1;
    for session in sessionList:
        print('[%d]' %(count), end="")
        count += 1
        print(session)

    if len(sessionList) == 0:
        print('No checkpoint sessions found')

def removeSession(sessionId = 0):
    print("TODO")
########################################################################
# VNC handling
########################################################################

def startGraphics():
    global vncserver_addr

    if vncserver_addr != -1:
        print('VNC server already running at: ' + vncserver_addr)
        return

    addr = 0
    while True:
        try:
            addr += 1
            out = subprocess.check_output(['vncserver', ':' + str(addr)],
                                          stderr=subprocess.STDOUT)
            os.environ['DISPLAY'] = ':' + str(addr)
            break
        except subprocess.CalledProcessError:
            pass
    vncserver_addr = addr

def showGraphics():
    global vncserver_addr

    if vncserver_addr == -1:
        print("VNC server not running.")
        return
    fnull = open(os.devnull, "w")
    saved_display = os.environ['DISPLAY']
    os.environ['DISPLAY'] = os.environ['ORIG_DISPLAY']
    out = subprocess.Popen(['dmtcp_nocheckpoint',
                            'vncviewer',
                            '-passwd', os.environ['HOME'] + '/.vnc/passwd',
                            ':' + str(vncserver_addr)],
                          stdout=fnull, stderr=fnull)
    os.environ['DISPLAY'] = saved_display

def stopGraphics():
    global vncserver_addr

    if vncserver_addr == -1:
        print("VNC server not running.")
        return

    try:
        out = subprocess.check_output(['vncserver', '-kill',
                                       ':' + str(vncserver_addr)],
                                      stderr=subprocess.STDOUT)
        del os.environ['DISPLAY']
    except subprocess.CalledProcessError:
        print('Error killing vncserver: ' + out)



if __name__ == '__main__':
    if isEnabled:
        print('DMTCP Status: Enabled')
        if isRunning():
            print('    isRunning: YES')
        else:
            print('    isRunning: NO')
        print('    numProcesses: ', numProcesses())
        print('    numCheckpoints: ', numCheckpoints())
        print('    numRestarts: ', numRestarts())
        print('    checkpointFilename: ', checkpointFilename())
    else:
        print('DMTCP Status: Disabled')
