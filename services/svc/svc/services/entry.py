import os, hashlib, shutil
from datetime import datetime, timedelta
import urllib
import http.client
import json
import re
import csv

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
         <li> <b>(S1)</b> ingest an executable (make sure services are on both servers)
         <p>
         <a href="{2}://{0}:{1}/svc/ingest?exe=/home/leipan/projects/dmtcp/git/navp/c/loop_with_hop">
         {2}://{0}:{1}/svc/ingest?exe=/home/leipan/projects/dmtcp/git/navp/c/loop_with_hop
         </a>.
         </p>
         </li>

         <li> <b>(S2)</b> hop by calling dmtcp_restart_script.sh (tbd: still need to call with both src_ip and dst_ip)
         <p>
         <a href="{2}://{0}:{1}/svc/hop?script=/home/leipan/projects/dmtcp/git/navp/services/svc/dmtcp_restart_script.sh">
         {2}://{0}:{1}/svc/hop?script=/home/leipan/projects/dmtcp/git/navp/services/svc/dmtcp_restart_script.sh
         </a>.
         </p>
         </li>

         <li> <b>(S3)</b> list jobs in job pool
         <p>
         <a href="{2}://{0}:{1}/svc/list_jobs?">
         {2}://{0}:{1}/svc/list_jobs
         </a>.
         </p>
         </li>

         <li> <b>(S4)</b> get job with id, or if no id is provided, get next job that is 'new' or 'ckpt'
         <p>
         <a href="{2}://{0}:{1}/svc/get_job?id=9">
         {2}://{0}:{1}/svc/get_job?id=9
         </a>.
         </p>
         <p>
         <a href="{2}://{0}:{1}/svc/get_job">
         {2}://{0}:{1}/svc/get_job
         </a>.
         </p>
         </li>

         <li> <b>(S5)</b> publish job with id
         <p>
         <a href="{2}://{0}:{1}/svc/publish_job?id=1&status=finished&dir=/home/ops/data/IND_CrIS_VIIRSMOD_SNDR.SNPP.20150601T1548.g159/">
         {2}://{0}:{1}/svc/publish_job?id=1&status=finished&dir=/home/ops/data/IND_CrIS_VIIRSMOD_SNDR.SNPP.20150601T1548.g159/
         </a>.
         </p>
         <p>
         <a href="{2}://{0}:{1}/svc/publish_job?id=2&status=ckpt">
         {2}://{0}:{1}/svc/publish_job?id=2&status=ckpt
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
  print('src_ip: ', src_ip)
  logger.info('src_ip: {0}'.format(src_ip))
  # dst_ip is where the computation is migrating to
  dst_ip = request.args.get('dst_ip', '')
  print('dst_ip: ', dst_ip)
  logger.info('dst_ip: {0}'.format(dst_ip))
  script = request.args.get('script', 'dmtcp_restart_script.sh')
  print('script: ', script)
  logger.info('script: {0}'.format(script))
  port = request.args.get('port', '6869')
  logger.info('port: {0}'.format(port))
  print('port: ', port)
  ckpt_filepath = request.args.get('ckpt', '')
  print('ckpt_filepath: ', ckpt_filepath)
  logger.info('ckpt_filepath: {0}'.format(ckpt_filepath))

  if src_ip=='' or dst_ip=='':
    dict1 = {'mesg':'need to call with both src_ip and dst_ip'}
    executionEndTime = float(time.time())
    print ('****** hop() elapsed time: ', executionEndTime - executionStartTime)
    logger.info('****** hop() elapsed time: %s' % str(executionEndTime - executionStartTime))
    return jsonify(dict1)


  # this service lives on the dst_ip
  # first get dmtcp_restart_script.sh and the ckpt file from src_ip to dst_ip (local)
  # location of files
  ### prefix = '/home/leipan/projects/dmtcp/git/navp/services/svc/'
  prefix = ''
  if ckpt_filepath != '':
    ckpt_basename = os.path.basename(ckpt_filepath)
    prefix = ckpt_filepath.replace(ckpt_basename, '')

  command_line = 'scp leipan@' + src_ip + ':' + prefix + script + ' ' + prefix + '.'
  args = shlex.split(command_line)
  ### print(args)
  p = subprocess.Popen(args)
  p.wait()

  ckpt_file = parse_script(os.path.join(prefix, script))[0]
  logger.info('ckpt_file: {0}'.format(ckpt_file))

  command_line = 'scp leipan@' + src_ip + ':' + ckpt_file + ' ' + prefix + '.'
  args = shlex.split(command_line)
  ### print(args)
  p = subprocess.Popen(args)
  p.wait()

  ckpt_files_dir = ckpt_file.replace('.dmtcp', '_files')
  logger.info('ckpt_files_dir: {0}'.format(ckpt_files_dir))

  command_line = 'scp -r leipan@' + src_ip + ':' + ckpt_files_dir + ' ' + prefix + '.'
  args = shlex.split(command_line)
  print(args)
  p = subprocess.Popen(args)
  p.wait()

  # then run dmtcp_restart_script.sh on dst_ip
  ### command_line = '/home/leipan/projects/dmtcp/git/navp/services/svc/dmtcp_restart_script.sh --coord-port ' + port
  print('port: ', port)
  print('dst_ip: ', dst_ip)
  ### command_line = 'dmtcp_restart_script.sh --coord-port ' + port + ' --coord-host ' + dst_ip
  command_line = prefix + 'dmtcp_restart_script.sh --coord-port ' + port + ' --coord-host localhost'
  args = shlex.split(command_line)
  print(args)
  p = subprocess.Popen(args)
  p.wait()

  dict1 = {'mesg':'dmtcp_restart_script.sh called'}

  executionEndTime = float(time.time())
  print ('****** hop() elapsed time: ', executionEndTime - executionStartTime)
  logger.info('****** hop() elapsed time: %s' % str(executionEndTime - executionStartTime))

  return jsonify(dict1)



def copytree(src, dst, symlinks=False, ignore=None):
  for item in os.listdir(src):
    s = os.path.join(src, item)
    d = os.path.join(dst, item)
    if os.path.isdir(s):
      shutil.copytree(s, d, symlinks, ignore)
    else:
      shutil.copy2(s, d)



# ------------------------------------------------
@app.route('/svc/publish_job', methods=["GET"])
@crossdomain(origin='*')
def publish_job():
  """Run publish_job"""
  logger.info('****** publish_job() starts.')
  executionStartTime = int(time.time())

  status = request.args.get('status', '')
  print('status: ', status)
  ### subdir1 = request.args.get('dir', '')
  ### print('subdir1: ', subdir1)
  job_id = request.args.get('id', '')
  print('job_id: ', job_id)

  jsonArray = []
  # open jobs.csv and read
      
  # read csv file
  csvFilePath = 'jobs.csv'
  with open(csvFilePath, encoding='utf-8') as csvf: 
    # load csv file data using csv library's dictionary reader
    csvReader = csv.DictReader(csvf) 

    # convert each csv row into python dict
    for row in csvReader: 
      # add this python dict to json array
      print('row: ', row)
      jsonArray.append(row)

  ### print('type(jsonArray): ', type(jsonArray))
  ### print('jsonArray[0]: ', jsonArray[0])

  if job_id == '': # create a new job with status
    # put status into next key of OrderedDict
    key1 = next(reversed(jsonArray[0]))
    print('recent key: ', key1)
    key2 = str(int(key1) + 1)
    print('next key: ', key2)
    jsonArray[0][key2] = status
    job_id = key2
  else: # update the job status
    jsonArray[0][job_id] = status
    key2 = job_id

  print(jsonArray[0])

  # write new OrderedDict back to jobs.csv
  keys, values = [], []
  for key, value in jsonArray[0].items():
    keys.append(key)
    values.append(value)

  with open(csvFilePath, "w") as outfile:
    csvwriter = csv.writer(outfile)
    csvwriter.writerow(keys)
    csvwriter.writerow(values)

  # mk subdir of id (key2)
  subdir2 = os.path.join('/home/ops/data/', key2)
  if not os.path.isdir(subdir2):
    os.mkdir(subdir2)

  dict1 = {'mesg':'job {0} published with status={1}'.format(job_id, status)}

  # if status is ckpt, copy dmtcp restart script to subdir id
  if status == 'ckpt':
    # copy dmtcp restart script to subdir id
    ### shutil.copyfile(os.path.join(subdir1, 'dmtcp_restart_script.sh'), os.path.join(subdir2, 'dmtcp_restart_script.sh'))
    ### print('copied {0} to {1}'.format(os.path.join(subdir1, 'dmtcp_restart_script.sh'), os.path.join(subdir2, 'dmtcp_restart_script.sh')))

    # parse restart script and copy dmtcp memory image file
    ### parsed_ckpt_files = parse_script(os.path.join(subdir2, 'dmtcp_restart_script.sh'))
    ### parsed_ckpt_file_basename = os.path.basename(parsed_ckpt_files[0])
    ### if os.path.exists(os.path.join(subdir2, parsed_ckpt_file_basename)):
      ### shutil.copyfile(os.path.join(subdir1, parsed_ckpt_file_basename), parsed_ckpt_file)
      ### print('copied {0} to {1}'.format(parsed_ckpt_file_basename, parsed_ckpt_file))
    print('check if dmtcp file exists in {}'.format(subdir2))

  elif status == 'finished':
    # copy product to subdir id
    ### print('subdir1: ', subdir1)
    print('subdir2: ', subdir2)
    ### copytree(subdir1, subdir2)


  executionEndTime = float(time.time())
  print ('****** publish_job() elapsed time: ', executionEndTime - executionStartTime)
  logger.info('****** publish_job() elapsed time: %s' % str(executionEndTime - executionStartTime))

  return jsonify(dict1)




# ------------------------------------------------
@app.route('/svc/list_jobs', methods=["GET"])
@crossdomain(origin='*')
def list_jobs():
  """Run list_jobs"""
  logger.info('****** list_jobs() starts.')
  executionStartTime = int(time.time())

  jsonArray = []
  # open jobs.csv and read
      
  #read csv file
  csvFilePath = 'jobs.csv'
  with open(csvFilePath, encoding='utf-8') as csvf: 
    #load csv file data using csv library's dictionary reader
    csvReader = csv.DictReader(csvf) 

    #convert each csv row into python dict
    for row in csvReader: 
      #add this python dict to json array
      print('row: ', row)
      jsonArray.append(row)

  ### print('type(jsonArray): ', type(jsonArray))
  ### print('jsonArray[0]: ', jsonArray[0])

  executionEndTime = float(time.time())
  print ('****** list_jobs() elapsed time: ', executionEndTime - executionStartTime)
  logger.info('****** list_jobs() elapsed time: %s' % str(executionEndTime - executionStartTime))

  return jsonify(sorted(jsonArray[0].items()))







# ------------------------------------------------
@app.route('/svc/get_job', methods=["GET"])
@crossdomain(origin='*')
def get_job():
  """Run get_job"""
  logger.info('****** get_job() starts.')
  executionStartTime = int(time.time())

  # get job status with job_id
  job_id = request.args.get('id', '')

  #read csv file
  jsonArray = []
  csvFilePath = 'jobs.csv'
  with open(csvFilePath, encoding='utf-8') as csvf: 
    #load csv file data using csv library's dictionary reader
    csvReader = csv.DictReader(csvf) 

    #convert each csv row into python dict
    for row in csvReader: 
      #add this python dict to json array
      ### print('row: ', row)
      jsonArray.append(row)

  ### print('type(jsonArray): ', type(jsonArray))
  ### print('jsonArray[0]: ', jsonArray[0])

  dict1 = {}

  # check status with job_id
  if job_id != '': # request provided a job_id
    try:
      dict1 = {job_id:jsonArray[0][job_id]}
      print(jsonArray[0][job_id])
    except KeyError:
      dict1 = {'mesg':'job with id={} does not exist yet'.format(job_id)}
  else: # request with no job_id, return first job that is 'ckpt' or 'new'
    for key, value in reversed(jsonArray[0].items()):
      if value == 'ckpt' or value == 'new':
        ### print('id: {0}, value: {1}'.format(id, value))
        dict1 = {key:value}

  executionEndTime = float(time.time())
  print ('****** get_job() elapsed time: ', executionEndTime - executionStartTime)
  logger.info('****** get_job() elapsed time: %s' % str(executionEndTime - executionStartTime))

  return jsonify(dict1)







# ------------------------------------------------
@app.route('/svc/hop2', methods=["GET"])
@crossdomain(origin='*')
def hop2():
  """Run hop2"""
  logger.info('****** svc/hop2 starts.')
  executionStartTime = int(time.time())

  # assume script is under ~/data
  # and the input is full path of the file
  script = request.args.get('script', 'dmtcp_restart_script.sh')
  print('script: ', script)
  logger.info('script: {0}'.format(script))
  port = request.args.get('port', '6869')
  logger.info('port: {0}'.format(port))
  print('port: ', port)
  # assume ckpt_filepath is under ~/data
  # and the input is full path of the dir
  ckpt_file = request.args.get('ckpt', '')
  print('ckpt_file: ', ckpt_file)
  logger.info('ckpt_file: {0}'.format(ckpt_file))

  # this service lives on the dst machine
  # first copy dmtcp_restart_script.sh and the ckpt file from ./data to local (./)
  script_path = os.path.join('/home/ops/data', script)
  print('script_path: ', script_path)
  parsed_ckpt_files = parse_script(script_path)
  parsed_ckpt_file_basename = os.path.basename(parsed_ckpt_files[0])
  # prefix is where the ckpt memory image is and is where the restart script is pointing at
  prefix = parsed_ckpt_files[0].replace(parsed_ckpt_file_basename, '')
  print('prefix: ', prefix)

  print('ckpt_file: ', ckpt_file)
  logger.info('ckpt_file: {0}'.format(ckpt_file))
  print('parsed_ckpt_files: ', parsed_ckpt_files)
  logger.info('parsed_ckpt_files: {0}'.format(parsed_ckpt_files))
  print('parsed_ckpt_file_basename: ', parsed_ckpt_file_basename)
  logger.info('parsed_ckpt_file_basename: {0}'.format(parsed_ckpt_file_basename))

  if parsed_ckpt_file_basename == ckpt_file:

    # copy dmtcp files from data/ to local dirs
    shutil.copyfile(script_path, './dmtcp_restart_script.sh')
    print('copied {} to ./dmtcp_restart_script.sh'.format(script_path))
    for f1 in parsed_ckpt_files:
      f1_basename = os.path.basename(f1)
      shutil.copyfile(os.path.join('/home/ops/data', f1_basename), os.path.join(prefix, f1_basename))
      print('copied {0} from /home/ops/data to {1}'.format(f1_basename, prefix))

    # then run dmtcp_restart_script.sh on dst_ip
    ### command_line = '/home/leipan/projects/dmtcp/git/navp/services/svc/dmtcp_restart_script.sh --coord-port ' + port
    print('port: ', port)
    ### print('dst_ip: ', dst_ip)
    ### command_line = 'dmtcp_restart_script.sh --coord-port ' + port + ' --coord-host ' + dst_ip
    command_line = 'sh ./dmtcp_restart_script.sh --coord-port ' + port + ' --coord-host localhost'
    print('command_line: ', command_line)

    args = shlex.split(command_line)
    print(args)
    restartStart = float(time.time())
    p = subprocess.Popen(args)
    p.wait()
    restartEnd = float(time.time())
    print ('*** restart elapsed time (includes restart overhead plus all the cost after restart): ', restartEnd - restartStart)

    dict1 = {'mesg':'dmtcp_restart_script.sh called'}
  else:
    dict1 = {'error':'dmtcp_restart_script.sh is pointing at the wrong dmtcp memory image'}

  executionEndTime = float(time.time())
  print ('****** svc/hop2 elapsed time: ', executionEndTime - executionStartTime)
  logger.info('****** svc/hop2 elapsed time: %s' % str(executionEndTime - executionStartTime))

  return jsonify(dict1)


