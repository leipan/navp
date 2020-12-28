import os, hashlib, shutil
from datetime import datetime, timedelta
import urllib
import http.client
import json
import re

import requests, time, json
import shlex, subprocess

import flask
from flask import jsonify, request, url_for, make_response
from flask import render_template
from werkzeug.utils import secure_filename

### from redis import Redis
### from rq import Queue

from svc import app
from svc.src.util.utils import (get_host_port, parse_script)

import logging
import logging.config
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename='navp_info.log')
### logging.basicConfig(level=logging.DEBUG, filename='navp_info.log')

from flask import current_app
from functools import update_wrapper
import traceback

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

### UPLOAD_FOLDER = '/home/svc/new_github/CMDA/JPL_CMDA/services/svc/svc/static/'
### app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# vicar cloud server
### STATIC = '/home/jpluser/github/CRISP_docker/docker/m2020_crisp/imgreg_services/services/svc/svc/static/'
### UTIL = '/home/jpluser/github/CRISP_docker/docker/m2020_crisp/imgreg_services/services/svc/svc/src/util/'
STATIC = '/home/jpluser/m2020_crisp/imgreg_services/services/svc/svc/static/'
UTIL = '/home/jpluser/m2020_crisp/imgreg_services/services/svc/svc/src/util/'

HEADERS = {'Content-Type': 'application/json'}

### hostcfg = '/home/jpluser/m2020_crisp/imgreg_services/services/svc/host.cfg'
### hostcfg = '/home/leipan/projects/dmtcp/git/navp/services/svc/host.cfg'
hostcfg = 'host.cfg'
protocol, server_ip, port_num = get_host_port(hostcfg)
vicar_ip = server_ip
vicar_port = port_num

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator



def url_is_alive(url):
  ### request = urllib2.Request(url)
  request = urllib.Request(url)
  print (request)
  request.get_method = lambda: 'HEAD'
  print (request.get_method)

  try:
    print (urllib.urlopen(request))
    return True
  except urllib.HTTPError:
    return False
  except urllib.URLError:
    return False


def exists(site, path):
  ### conn = httplib.HTTPConnection(site)
  conn = http.client.HTTPConnection(site)
  conn.request('HEAD', path)
  response = conn.getresponse()
  conn.close()
  return response.status == 200


# ------------------------------------------------
@app.route('/')
def hello():

  protocol, server_ip, port_num = get_host_port(hostcfg)
  print ('protocol: ', protocol)
  print ('server_ip: ', server_ip)
  print ('port_num: ', port_num)
  logger.info('protocol: {0}'.format(protocol))

  vicar_ip = server_ip
  vicar_port = port_num

  mesg = """
         <!DOCTYPE html>
         <html>
         <head>
         <title>NAVP Bridging Services</title>
         </head>
         <body>
         <h3>
         Welcome to the NAVP Bridging Services.
         </h3>

         <p>
         The NAVP Bridging Services are built based on NAVP and DMTCP.
         </p>

         <p>
         <h4>NAVP Bridging Rest Examples:</h4>
         </p>

         <ul>
         <li> <b>(S1)</b> ingest an executable
         <p>
         <a href="{0}:{1}/svc/ingest?exe=hop_example">
         {0}:{1}/svc/ingest?script=hop_example
         </a>.
         </p>
         </li>

         <li> <b>(S2)</b> hop by calling dmtcp_restart_script.sh
         <p>
         <a href="{0}:{1}/svc/hop?script=dmtcp_restart_script.sh">
         {0}:{1}/svc/hop?script=dmtcp_restart_script.sh
         </a>.
         </p>
         </li>
         </ul>

         <br>

         <p>
         For more information, please  
         <a href="mailto:leipan@jpl.nasa.gov">email me</a>. 
         </p>
         </body>
         </html>

         <br>

         """.format(server_ip, port_num, protocol, vicar_ip, vicar_port)
  logger.info('CRISP up and running.')
  return mesg



# ------------------------------------------------
@app.route('/svc/ingest', methods=["GET"])
@crossdomain(origin='*')
def ingest():
  """Run ingest"""
  logger.info('****** ingest() starts.')
  executionStartTime = int(time.time())

  executable = request.args.get('exe', '')
  logger.info('executable: {0}'.format(executable))

  DMTCP_ROOT = os.environ.get('DMTCP_ROOT')
  DEMO_PORT = os.environ.get('DEMO_PORT')

  # ingest always assumes that the executable resides locally
  ### dmtcp = DMTCP_ROOT+'/bin/dmtcp_launch --quiet --coord-port '+DEMO_PORT+' --with-plugin libdmtcp_plugin-to-announce-events.so '
  dmtcp = DMTCP_ROOT+'/bin/dmtcp_launch --quiet --coord-port '+DEMO_PORT+' '
  command_line = dmtcp + executable

  # run with dmtcp_launch
  args = shlex.split(command_line)
  print(args)
  p = subprocess.Popen(args)
  p.wait()

  dict1 = {'mesg':'{} ingested'.format(executable)}

  executionEndTime = float(time.time())
  print ('****** ingest() elapsed time: ', executionEndTime - executionStartTime)
  logger.info('****** ingest() elapsed time: %s' % str(executionEndTime - executionStartTime))

  return jsonify(dict1)



# ------------------------------------------------
@app.route('/svc/hop', methods=["GET"])
@crossdomain(origin='*')
def hop():
  """Run hop"""
  logger.info('****** hop() starts.')
  executionStartTime = int(time.time())

  # src_ip is where the computation is from
  src_ip = request.args.get('src_ip', '')
  logger.info('src_ip: {0}'.format(src_ip))
  # dst_ip is where the computation is migrating to
  dst_ip = request.args.get('dst_ip', '')
  logger.info('dst_ip: {0}'.format(dst_ip))
  script = request.args.get('script', 'dmtcp_restart_script.sh')
  logger.info('script: {0}'.format(script))
  port = request.args.get('port', '6869')
  logger.info('port: {0}'.format(port))

  if src_ip=='' or dst_ip=='':
    dict1 = {'mesg':'need to call with both src_ip and dst_ip'}
    executionEndTime = float(time.time())
    print ('****** hop() elapsed time: ', executionEndTime - executionStartTime)
    logger.info('****** hop() elapsed time: %s' % str(executionEndTime - executionStartTime))
    return jsonify(dict1)

  print('port: ', port)
  print('src_ip: ', src_ip)
  print('dst_ip: ', dst_ip)

  # this service lives on the dst_ip
  # first get dmtcp_restart_script.sh and the ckpt file from src_ip to dst_ip (local)
  # location of files
  prefix = '/home/leipan/projects/dmtcp/git/navp/services/svc/'
  command_line = 'scp leipan@' + src_ip + ':' + prefix + script + ' .'
  args = shlex.split(command_line)
  print(args)
  p = subprocess.Popen(args)
  p.wait()

  ckpt_file = parse_script(script)
  logger.info('ckpt_file: {0}'.format(ckpt_file))

  command_line = 'scp leipan@' + src_ip + ':' + ckpt_file + ' .'
  args = shlex.split(command_line)
  print(args)
  p = subprocess.Popen(args)
  p.wait()

  # then run dmtcp_restart_script.sh on dst_ip
  ### command_line = '/home/leipan/projects/dmtcp/git/navp/services/svc/dmtcp_restart_script.sh --coord-port ' + port
  print('port: ', port)
  print('dst_ip: ', dst_ip)
  ### command_line = 'dmtcp_restart_script.sh --coord-port ' + port + ' --coord-host ' + dst_ip
  command_line = 'dmtcp_restart_script.sh --coord-port ' + port + ' --coord-host localhost'
  args = shlex.split(command_line)
  print(args)
  p = subprocess.Popen(args)
  p.wait()

  dict1 = {'mesg':'dmtcp_restart_script.sh called'}

  executionEndTime = float(time.time())
  print ('****** hop() elapsed time: ', executionEndTime - executionStartTime)
  logger.info('****** hop() elapsed time: %s' % str(executionEndTime - executionStartTime))

  return jsonify(dict1)



