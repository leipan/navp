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
  print ('fname: ', fname)

  ### if dmtcp.isResume():
  if isResume():
    restart_cmd = \
      'curl "http://{0}:8080/svc/hop?src_ip={1}&dst_ip={2}&port={3}&ckpt={4}" '.format(dst_ip, src_ip, dst_ip, port, fname)
    print('restart_cmd: ', restart_cmd)

    args = shlex.split(restart_cmd)
    print(args)
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
