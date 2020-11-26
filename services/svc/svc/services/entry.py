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
from svc.src.util.utils import (get_host_port)

import logging
import logging.config
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, filename='crisp_info.log')
### logging.basicConfig(level=logging.DEBUG, filename='crisp_info.log')

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
hostcfg = '/home/leipan/projects/dmtcp/git/navp/services/svc/host.cfg'
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

         <li> <b>(I1)</b> calling dmtcp_restart_script.sh
         <p>
         <a href="{3}://{0}:{1}/svc/navp_hop?script=dmtcp_restart_script.sh">
         {3}://{0}:{1}/svc/navp_hop?script=dmtcp_restart_script.sh
         </a>.
         </p>
         </li>




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
@app.route('/svc/navp', methods=["GET"])
@crossdomain(origin='*')
def navp():
    """Run navp"""
    logger.info('****** navp() starts.')
    executionStartTime = int(time.time())

    dict1 = {'mesg':'navp up and running'}

    executionEndTime = float(time.time())
    print ('****** navp() elapsed time: ', executionEndTime - executionStartTime)
    logger.info('****** navp() elapsed time: %s' % str(executionEndTime - executionStartTime))

    return jsonify(dict1)



