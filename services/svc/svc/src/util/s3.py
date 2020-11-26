#!/usr/bin/env python

import sys, os
import boto3, botocore
from botocore.exceptions import ClientError
import re
import flask
import base64
import json
import logging

logger = logging.getLogger(__name__)



# ------------------------------------------------
def get_s3_creds():

  logger.info('getting s3 creds ...')

  try:
    s3_creds = flask.request.headers.get('X-AWS')
    s3_creds = json.loads(base64.b64decode(s3_creds))
    logger.info('s3_creds: {}'.format(json.dumps(s3_creds, indent=2)))

  except botocore.exceptions.NoCredentialsError as e:
    return 'botocore.exceptions.NoCredentialsError'
  except botocore.exceptions.EndpointConnectionError as e:
    return 'botocore.exceptions.EndpointConnectionError'

  return s3_creds


# ------------------------------------------------
def check_s3_file(bucket_name, key, s3_creds):

  logger.info('checking s3 file ...')
  logger.info('bucket_name: {}'.format(bucket_name))
  logger.info('key: {}'.format(key))

  try:
    session = boto3.Session(aws_access_key_id=s3_creds['id'],
                            aws_secret_access_key=s3_creds['secret'],
                            aws_session_token=s3_creds['session'],
                            region_name=s3_creds['region'])
    s3 = session.resource('s3')

    logger.info('before load() ...')
    s3.Bucket(bucket_name).Object(key).load()
    logger.info('after load()')

  except ClientError as e:
    return int(e.response['Error']['Code']) != 404
  except botocore.exceptions.EndpointConnectionError as e:
    return 'botocore.exceptions.EndpointConnectionError'

  return True


# ------------------------------------------------
def check(bucket_name, key):

  logger.info('getting in s3.check() ...')
  logger.info('bucket_name: {}'.format(bucket_name))
  logger.info('key: {}'.format(key))

  try:
    s3_creds = flask.request.headers.get('X-AWS')
    s3_creds = json.loads(base64.b64decode(s3_creds))
    logger.info('s3_creds: {}'.format(json.dumps(s3_creds, indent=2)))
    session = boto3.Session(aws_access_key_id=s3_creds['id'],
                            aws_secret_access_key=s3_creds['secret'],
                            aws_session_token=s3_creds['session'],
                            region_name=s3_creds['region'])
    s3 = session.resource('s3')

    ### s3 = boto3.resource('s3')

    logger.info('before load() ...')
    s3.Bucket(bucket_name).Object(key).load()
    logger.info('after load()')

  except ClientError as e:
    return int(e.response['Error']['Code']) != 404
  except botocore.exceptions.NoCredentialsError as e:
    return 'botocore.exceptions.NoCredentialsError'
  except botocore.exceptions.EndpointConnectionError as e:
    return 'botocore.exceptions.EndpointConnectionError'

  return True


# ------------------------------------------------
def parse_s3_url(url):
  # example: 'https://s3-us-gov-west-1.amazonaws.com/m2020imgcoregi/MR0_513349668EDR_S0540010MCAM06203M1.IMG'
  #          'https://s3-us-gov-west-1.amazonaws.com/m20-dev-ids-datadrive-bucket01/m20-edr-rdr-test/00630/opgs/rdr/ncam/NLB_453423385RASLF0311472NCAM00276M1.IMG'
  # or
  #          's3://m2020imgcoregi/MR0_513349668EDR_S0540010MCAM06203M1.IMG'

  # add trailing '/' if not there
  if not url.endswith('/'):
    url = url + '/'

  # aws url
  if url.startswith('https://'):
    # location
    r1 = re.search('s3-(.*).amazonaws.com', url)
    bucket_location = r1.group(1)

    # bucket name plus file name then split to get bucket name
    r2 = re.search('amazonaws.com/(.*)/', url)
    bucket_name = r2.group(1)
    bucket_name = re.split('/', bucket_name)[0]

    # bucket name plus file name then remove bucket name
    r3 = re.search('amazonaws.com/(.*)/', url)
    str1 = r3.group(1)
    file_name = str1.replace(bucket_name+'/', '')
  # s3 url
  elif url.startswith('s3://'):
    bucket_location = ''

    # bucket name plus file name then split to get bucket name
    r2 = re.search('s3://(.*)/', url)
    bucket_name = r2.group(1)
    bucket_name = re.split('/', bucket_name)[0]

    # bucket name plus file name then remove bucket name
    r3 = re.search('s3://(.*)/', url)
    str1 = r3.group(1)
    file_name = str1.replace(bucket_name+'/', '')
  else:
    bucket_location = ''
    bucket_name = ''
    file_name = ''

  return bucket_location, bucket_name, file_name



# ------------------------------------------------
# the input: bucket, filename, and s3_creds 
def s3_file_download(bucket_name, filename, filepath, s3_creds):

  logger.info('getting in s3.s3_download() ...')
  logger.info('bucket_name: {}'.format(bucket_name))
  logger.info('filename: {}'.format(filename))
  logger.info('filepath: {}'.format(filepath))

  try:
    # Create an S3 client
    session = boto3.Session(aws_access_key_id=s3_creds['id'],
                            aws_secret_access_key=s3_creds['secret'],
                            aws_session_token=s3_creds['session'],
                            region_name=s3_creds['region'])
    s3 = session.resource('s3')

    logger.info('in s3_download(), before load() ...')
    logger.info('bucket_name: {0}, filename: {1}, filepath: {2}'.format(bucket_name, filename, filepath))
    s3.Bucket(bucket_name).Object(filename).load()
    logger.info('after load()')

    s3.Bucket(bucket_name).download_file(filename, filepath)
    return 'downloaded ' + filename
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
      print("The object does not exist.")
    else:
      ### raise
      logger.info('s3_download() failed')
      print('s3_download() failed')
      return 's3_download() failed'
  except botocore.exceptions.NoCredentialsError as e:
    return 'botocore.exceptions.NoCredentialsError'



# ------------------------------------------------
# the input is KEY
def s3_download(bucket_name, filename, filepath):

  logger.info('getting in s3.s3_download() ...')
  logger.info('bucket_name: {}'.format(bucket_name))
  logger.info('filename: {}'.format(filename))
  logger.info('filepath: {}'.format(filepath))

  try:
    # Create an S3 client
    s3_creds = flask.request.headers.get('X-AWS')
    s3_creds = json.loads(base64.b64decode(s3_creds))
    session = boto3.Session(aws_access_key_id=s3_creds['id'],
                            aws_secret_access_key=s3_creds['secret'],
                            aws_session_token=s3_creds['session'],
                            region_name=s3_creds['region'])
    s3 = session.resource('s3')

    logger.info('in s3_download(), before load() ...')
    logger.info('bucket_name: {0}, filename: {1}, filepath: {2}'.format(bucket_name, filename, filepath))
    s3.Bucket(bucket_name).Object(filename).load()
    logger.info('after load()')

    s3.Bucket(bucket_name).download_file(filename, filepath)
    return 'downloaded ' + filename
  except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
      print("The object does not exist.")
    else:
      ### raise
      logger.info('s3_download() failed')
      print('s3_download() failed')
      return 's3_download() failed'
  except botocore.exceptions.NoCredentialsError as e:
    return 'botocore.exceptions.NoCredentialsError'



# ------------------------------------------------
def s3_file_upload(bucket_location, bucket_name, filename, filepath, s3_creds):

  try:
    # Create an S3 client
    session = boto3.Session(aws_access_key_id=s3_creds['id'],
                            aws_secret_access_key=s3_creds['secret'],
                            aws_session_token=s3_creds['session'],
                            region_name=s3_creds['region'])
    s3 = session.resource('s3')

    ### s3 = boto3.resource('s3')

    # the 3rd arg is a key
    ### s3.upload_file(filepath, bucket_name, filename, ExtraArgs={'ACL': 'public-read'})
    s3.meta.client.upload_file(filepath, bucket_name, filename, ExtraArgs=None)

    """
    obj1 = s3.Object(bucket_name, filename)
    object_acl = obj1.Acl()
    print ('acl:', object_acl)
    """

    ### bucket_location = 'us-gov-west-1'
    s3_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location, bucket_name, filename)
    ### print ('s3_url: ', s3_url)

    return {'mesg':'s3 upload succeeded', 'url':s3_url}
  except botocore.exceptions.ClientError as err:
    if err.response['Error']['Code'] == 'ExpiredToken':
      print("AWS Token expired. Renew and retry")
      return {'mesg':'s3 upload failed. AWS Token expired.', 'url':''}

    if err.response['Error']['Code'] == 'AccessDenied':
      print("Access denied. Check AWS Token and retry")
      return {'mesg':'s3 upload failed. Access denied.', 'url':''}
  except botocore.exceptions.NoCredentialsError as err:
    print('No credentials for s3 access.')
    return {'mesg':'No credentials for s3 access.', 'url':''}
  except boto3.exceptions.S3UploadFailedError as err:
    print('Failed to upload to s3.')
    return {'mesg':'s3 upload failed.', 'url':''}



# ------------------------------------------------
def s3_upload(bucket_location, bucket_name, filename, filepath):

  try:
    # Create an S3 client
    s3_creds = flask.request.headers.get('X-AWS')
    s3_creds = json.loads(base64.b64decode(s3_creds))
    session = boto3.Session(aws_access_key_id=s3_creds['id'],
                            aws_secret_access_key=s3_creds['secret'],
                            aws_session_token=s3_creds['session'],
                            region_name=s3_creds['region'])
    s3 = session.resource('s3')

    ### s3 = boto3.resource('s3')

    # the 3rd arg is a key
    ### s3.upload_file(filepath, bucket_name, filename, ExtraArgs={'ACL': 'public-read'})
    s3.meta.client.upload_file(filepath, bucket_name, filename, ExtraArgs=None)

    """
    obj1 = s3.Object(bucket_name, filename)
    object_acl = obj1.Acl()
    print ('acl:', object_acl)
    """

    ### bucket_location = 'us-gov-west-1'
    s3_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(bucket_location, bucket_name, filename)
    ### print ('s3_url: ', s3_url)

    return {'mesg':'s3 upload succeeded', 'url':s3_url}
  except botocore.exceptions.ClientError as err:
    if err.response['Error']['Code'] == 'ExpiredToken':
      print("AWS Token expired. Renew and retry")
      return {'mesg':'s3 upload failed. AWS Token expired.', 'url':''}

    if err.response['Error']['Code'] == 'AccessDenied':
      print("Access denied. Check AWS Token and retry")
      return {'mesg':'s3 upload failed. Access denied.', 'url':''}
  except botocore.exceptions.NoCredentialsError as err:
    print('No credentials for s3 access.')
    return {'mesg':'No credentials for s3 access.', 'url':''}
  except boto3.exceptions.S3UploadFailedError as err:
    print('Failed to upload to s3.')
    return {'mesg':'s3 upload failed.', 'url':''}


# ------------------------------------------------
def upload_file(bucket_location, bucket, file_name, file_path):
    # Upload a file to an S3 bucket

    # Upload the file
    s3_client = boto3.client('s3')
    try:
      response = s3_client.upload_file(file_path, bucket, file_name)
    except ClientError as e:
      logging.error(e)
      return False
    return True


# ------------------------------------------------
def s3_bucket_location():

  try:
    s3_creds = flask.request.headers.get('X-AWS')
    s3_creds = json.loads(base64.b64decode(s3_creds))
    session = boto3.Session(aws_access_key_id=s3_creds['id'],
                            aws_secret_access_key=s3_creds['secret'],
                            aws_session_token=s3_creds['session'],
                            region_name=s3_creds['region'])
    s3 = session.resource('s3')

    ### bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)
    bucket_location = s3.get_bucket_location(Bucket=bucket_name)
    return {'bucket_location':bucket_location, 'mesg':'obtain bucket_location succeeded'}
  except botocore.exceptions.ClientError as err:
    if err.response['Error']['Code'] == 'ExpiredToken':
      print("AWS Token expired. Renew and retry")
      return {'bucket_location':'', 'mesg':'obtain bucket_location failed'}

    if err.response['Error']['Code'] == 'AccessDenied':
      print("Access denied. Check AWS Token and retry")
      return {'bucket_location':'', 'mesg':'obtain bucket_location failed'}
  except botocore.exceptions.NoCredentialsError as e:
    return {'error':'botocore.exceptions.NoCredentialsError'}


# ------------------------------------------------
if __name__ == '__main__':

  ### s3 = boto3.resource('s3')

  """
  bucket_location = 'us-gov-west-1'
  bucket_name = 'm2020imgcoregi'

  print('see if s3.py exists on s3')
  print(check(bucket_name, 's3.py'))
  print('see if abc.txt exists on s3')
  print(check(bucket_name, 'abc.txt'))
  """

  ### output1 = './MR0_513349668EDR_S0540010MCAM06203M1.IMG'
  ### outputname =  'MR0_513349668EDR_S0540010MCAM06203M1.IMG'

  ### outputname = 'CH4_AIRS_init_100.0_2006-01-01_to_2006-01-31_dot.png'
  """
  outputname = 'NRB_516985048ILT_F0541490NCAM00353M1.IMG'
  output1 = './' + outputname
  if os.path.exists(output1):
    s3_upload(bucket_location, bucket_name, outputname, output1)
  else:
    print('The file being uploaded does not exist locally.')
  """

  ### filename1 = 'MR0_513349668EDR_S0540010MCAM06203M1.IMG'
  """
  filename1 = outputname
  filepath1 = '/home/jpluser/tmp/' + filename1
  if(check(bucket_name, filename1)):
    s3_download(bucket_name, filename1, filepath1)
  else:
    print('The file being downloaded does not exist on S2.')
  """

  ### print (s3_bucket_location())

  url = 'https://s3-us-gov-west-1.amazonaws.com/m2020imgcoregi/images/NRB_516985048ILT_F0541490NCAM00353M1.IMG'
  print ('url: ', url)

  bucket_location, bucket_name, filename = parse_s3_url(url)
  print('bucket_location: ', bucket_location)
  print('bucket_name: ', bucket_name)
  print('filename: ', filename)

  print(check(bucket_name, filename))

  url = 'https://s3-us-gov-west-1.amazonaws.com/m20-dev-ids-datadrive-bucket01/m20-edr-rdr-test/00630/opgs/rdr/ncam/NLB_453423385RASLF0311472NCAM00276M1.IMG'
  print ('url: ', url)

  bucket_location, bucket_name, filename = parse_s3_url(url)
  print('bucket_location: ', bucket_location)
  print('bucket_name: ', bucket_name)
  print('filename: ', filename)

  print(check(bucket_name, filename))

