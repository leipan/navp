import numpy as np
import glob
import geo_QY
import time
import pdb
import os, sys
import requests
import pickle
import shutil
import netCDF4 as nc4
from datetime import datetime
import dmtcp
import json
sys.path.append('/home/ops/navp/services/svc/svc/src/util')
from utils import get_host_port

# note:
# this script is run from navp/python/
# and the input/output are placed in /home/ops/data/ in the docker container

def get_ips():
  ### ip1 = "weather2.jpl.nasa.gov"
  ### ip2 = "higgs.jpl.nasa.gov"

  protocol, hostname, port = get_host_port('/home/ops/navp/services/svc/host.cfg')
  print('port: ', port)

  ip2 = "127.0.0.1:28080"
  ip1 = "127.0.0.1:8080"

  if port in ip1:
    src_ip = ip1
    dst_ip = ip2
  else:
    src_ip = ip2
    dst_ip = ip1

  ### print('src_ip: ', src_ip)
  ### print('dst_ip: ', dst_ip)

  return src_ip, dst_ip
    
      
def swap_ips(src_ip, dst_ip):
  return dst_ip, src_ip







def main(job_id):
    dataDir2='/home/ops/data/'
    dataDir4='/home/ops/data/'
    
    if True:
        cris_geo_files = sorted(glob.glob(dataDir2+'SNDR.SNPP.CRIS*'))
        print ('cris_geo_files: ', cris_geo_files)
        viirs_geo_files = sorted(glob.glob(dataDir4+'VNP03MOD*A*'+'*'))
        print ('viirs_geo_files: ', viirs_geo_files)

        # read VIIRS data 
        viirs_lon, viirs_lat, viirs_satAzimuth, viirs_satRange, viirs_satZenith, viirs_height, viirs_time = geo_QY.read_nasa_viirs_geo(viirs_geo_files)
        ### print ('viirs_time: ', viirs_time)
        ### print ('type(viirs_time): ', type(viirs_time))
        ### print ('viirs_time: ', viirs_time)
        print ('viirs_time.shape: ', viirs_time.shape)
        ### print ('viirs_time.min(): ', viirs_time.min())
        ### print ('viirs_time.max(): ', viirs_time.max())

        ### print ('viirs_lon: ', viirs_lon)
        ### print ('type(viirs_lon): ', type(viirs_lon))
        print ('viirs_lon.shape: ', viirs_lon.shape)

        start_time = viirs_time.min()
        end_time = viirs_time.max()

        # read CrIS data 
        cris_lon, cris_lat, cris_satAzimuth, cris_satRange, cris_satZenith, cris_time, cris_realLW = geo_QY.read_nasa_cris_geo(cris_geo_files)
        ### print ('cris_time: ', cris_time)
        print ('cris_time.min(): ', cris_time.min())
        print ('cris_time.max(): ', cris_time.max())

        if start_time < cris_time.min():
          start_time = cris_time.min()

        if end_time > cris_time.max():
          end_time = cris_time.max()

        print ('start_time: ', start_time)
        print ('end_time: ', end_time)

        ### dmtcp.hop2(src_ip, dst_ip, port)
        dmtcp.publish(src_ip, dst_ip, port, 'ckpt', job_id)

        ### sys.exit(0)


        # CrIS and VIIRS use epoch time since 1/1/1993 (1993TAI),
        # and unix epoch time is since 1/1/1970
        # there is a 23 year difference
        diff = (datetime(1993,1,1,0,0) - datetime(1970,1,1)).total_seconds()
        print('diff: ', diff)

        time.sleep(15)

        start_time += diff
        end_time += diff

        os.environ['TZ'] = 'GMT'
        time.tzset()
        start_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(start_time))
        end_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.localtime(end_time))

        print ('start_date: ', start_date)
        print ('end_date: ', end_date)

        start_date2 = time.strftime('%Y%m%dT%H%M%S', time.localtime(start_time))
        end_date2 = time.strftime('%Y%m%dT%H%M%S', time.localtime(end_time))

        print ('start_date2: ', start_date2)
        print ('end_date2: ', end_date2)

        # changed per Qing's suggestion
        ### output_filename = 'IND_CrIS_VIIRSMOD_' + start_date2 + '_' + end_date2

        # Qing's suggestion:
        # use this name: IND_CrIS_VIIRSMOD_SNDR.SNPP.20150601T1548.g159.nc
        # for this CRIS granule: SNDR.SNPP.CRIS.20150601T1548.m06.g159.L1B_NSR.std.v02_05.G.180904193415.nc
        cris_geo_file = os.path.basename(cris_geo_files[0])
        print ('cris_geo_file: ', cris_geo_file)
        split1 = cris_geo_file.split('.')
        print ('split1: ', split1)
        # split1:  ['SNDR', 'SNPP', 'CRIS', '20150603T1836', 'm06', 'g187', 'L1B_NSR', 'std', 'v02_05', 'G', '180905023033', 'nc']

        outDir='/home/ops/data/' + job_id

        output_filename = 'IND_CrIS_VIIRSMOD_' + split1[0] + '.' + split1[1] + '.' + split1[3] + '.' + split1[5]
        print ('output_filename: ', output_filename)

        """
        if os.path.exists(outDir):
          shutil.rmtree(outDir)
        """

        output_dir = os.path.join(outDir, output_filename)
        print('output_dir: ', output_dir)
        if not os.path.isdir(output_dir):
          print('makedirs ... {}'.format(output_dir))
          os.makedirs(output_dir)

        # compute CrIS Pos Vector in EFEC on the Earth Surface 
        cris_pos= np.zeros(np.append(cris_lat.shape, 3))
        cris_pos[:, :, :, 0], cris_pos[:, :, :, 1], cris_pos[:, :, :, 2] \
	    = geo_QY.LLA2ECEF(cris_lon, cris_lat, np.zeros_like(cris_lat))

        # compute CrIS LOS Vector in ECEF 
        cris_east, cris_north, cris_up = geo_QY.RAE2ENU(cris_satAzimuth, cris_satZenith, cris_satRange)

        cris_los= np.zeros(np.append(cris_lat.shape, 3))
        cris_los[:, :, :, 0], cris_los[:, :, :, 1], cris_los[:, :, :, 2] = \
	    geo_QY.ENU2ECEF(cris_east, cris_north, cris_up, cris_lon, cris_lat)

        print ('cris_los.shape: ', cris_los.shape)

        # compute viirs POS vector in ECEF
        viirs_pos= np.zeros(np.append(viirs_lat.shape, 3))
        viirs_pos[:, :, 0], viirs_pos[:, :, 1], viirs_pos[:, :, 2] = \
	    geo_QY.LLA2ECEF(viirs_lon, viirs_lat, np.zeros_like(viirs_lat))

        print ('viirs_pos.shape: ', viirs_pos.shape)

        # cris_los is pointing from pixel to satellite, we need to
        #   change from satellite to pixel
        cris_los = -1.0*cris_los

        # using Kd-tree to find the closted pixel of VIIRS for each CrIS FOV
        # Set fake viirs_sdrQa to be zero: good quality everywhere since not for calibration
        #viirs_sdrQa=np.zeros(viirs_lon.shape)

        #remove the sdrqa, but adding time requirement (less than 600S difference)
        dy, dx = geo_QY.match_cris_viirs_QY(cris_los, cris_pos, viirs_pos, cris_time, viirs_time)

        ### dmtcp.hop2(dst_ip, src_ip, port+1)

        ### print ('dy: ', dy)
        print ('dy.shape: ', dy.shape)
        ### print ('dx: ', dx)
        print ('dx.shape: ', dx.shape)

        # print("collocation are done in --- %s seconds --- for %d files " % (time.time() - start_time, len(cris_geo_files)))

        dy_flatten = np.array([item for lst in dy.reshape(-1) for item in lst])
        dy_size = np.array([len(lst) for lst in dy.reshape(-1)]).reshape(dy.shape)
        dx_flatten = np.array([item for lst in dx.reshape(-1) for item in lst])

        ### f = nc4.Dataset('/raid15/qyue/VIIRS/VIIRS/201501/Index/IND_CrIS_VIIRSMOD_201501'+str(iday)+'_'+str(iloop)+'.nc','w', format='NETCDF4') #'w' stands for write
        ### f = nc4.Dataset('/raid15/leipan/VIIRS/VIIRS/201501/Index/IND_CrIS_VIIRSMOD_201501'+str(iday)+'_'+str(iloop)+'.nc','w', format='NETCDF4') #'w' stands for write
        ### f = nc4.Dataset('./IND_CrIS_VIIRSMOD_201501'+'.nc','w', format='NETCDF4') #'w' stands for write

        # make it a real standard netcdf product
        # e.g., include long name of all the variables

        output_filepath = os.path.join(outDir, output_filename, output_filename+'.nc')
        ### f = nc4.Dataset(outDir+output_filename+'/'+output_filename+'.nc','w', format='NETCDF4') #'w' stands for write
        f = nc4.Dataset(output_filepath, 'w', format='NETCDF4') #'w' stands for write

        f.createDimension('m',dy_flatten.size)
        f.createDimension('x', dy.shape[0])
        f.createDimension('y', dy.shape[1])
        f.createDimension('z', dy.shape[2])

        y_flatten = f.createVariable('dy', 'i4', ('m',))
        y_flatten.setncatts({'long_name':u'y coords', 'units':u'meter', 'var_desc':u'Y coordnates'})
        y_size=f.createVariable('dy_size','i4',('x', 'y', 'z',))
        y_size.setncatts({'long_name':u'y size', 'units':u'none', 'var_desc':u'Y dimension size'})
        x_flatten = f.createVariable('dx', 'i4', ('m',))
        x_flatten.setncatts({'long_name':u'x coords', 'units':u'meter', 'var_desc':u'X coordnates'})

        print ('dx_flatten.shape: ', dx_flatten.shape)

        y_size[:]=dy_size
        y_flatten[:]=dy_flatten
        x_flatten[:]=dx_flatten

        # add global attributes

        viirs_str = ''
        for item1 in viirs_geo_files:
          viirs_str += ',' + os.path.basename(item1)

        viirs_str = viirs_str[1:]
        f.viirs_file_names = viirs_str

        ### f.cris_file_name = os.path.basename(cris_geo_file)
        cris_str = ''
        for item1 in cris_geo_files:
          cris_str += ',' + os.path.basename(item1)

        cris_str = cris_str[1:]
        f.cris_file_names = cris_str

        f.cris_start_time = start_date
        f.cris_end_time = end_date

        f.cris_min_lat = cris_lat.min()
        f.cris_min_lon = cris_lon.min()
        f.cris_max_lat = cris_lat.max()
        f.cris_max_lon = cris_lon.max()


        f.description="Co-location Data for 2015 Jan"

        f.close()


    # datetime object containing current date and time
    now = datetime.now()
    print("now: ", now)

    # dd/mm/YY H:M:S
    ### dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    dt_string = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    print("date and time =", dt_string)	

    d1 = \
    {
        "creation_timestamp": dt_string,
        "version": "v1.0",
        "starttime": start_date,
        "endtime": end_date,
        "label": "matchup_cris_viirs_"+ start_date2 + '_' + end_date2
    }
    output_filepath2 = os.path.join(outDir, output_filename, output_filename+'.dataset.json')
    with open(output_filepath2, 'w') as datasetf:
        json.dump(d1, datasetf, indent=2)

    d2 = {}
    output_filepath3 = os.path.join(outDir, output_filename, output_filename+'.met.json')
    with open(output_filepath3, 'w') as metf:
        json.dump(d2, metf, indent=2)

    dmtcp.publish(src_ip, dst_ip, port+1, 'finished', job_id)

    print("started at: ", start_t)
    print("now at: ", float(time.time()))
    print("done in --- %.2f seconds --- " % (float(time.time() - start_t)))

    # collocation is done
# end of main()


if __name__ == '__main__':


    start_t = time.time()
    print ('current dir: ', os.getcwd())

    """
    if not dmtcp.isEnabled:
      print('Run with dmtcp, like this: dmtcp_launch python %s'%__file__)
      sys.exit(-1)
    """

    src_ip, dst_ip = get_ips()
    print('src_ip: ', src_ip)
    print('dst_ip: ', dst_ip)
    port = 7788

    job_id = '9'
    ### dst_ip = 'http://higgs.jpl.nasa.gov:8080/'

    # get job with id
    cmd = 'http://{0}/svc/get_job?id={1}'.format(dst_ip, job_id)

    # get next job that is 'new' or 'ckpt'
    cmd = 'http://{0}/svc/get_job'.format(dst_ip)

    print('cmd: ', cmd)

    x = requests.get(cmd)
    print(x.text)
    y = json.loads(x.text)
    ### status = y[job_id]

    dict_pairs = y.items()
    pairs_iterator = iter(dict_pairs)
    first_pair = next(pairs_iterator)
    print(type(first_pair))

    job_id = first_pair[0]
    print('job_id: ', job_id)
    status = first_pair[1]
    print('status: ', status)

    if status == 'new':
      # run the app from beginning
      main(job_id)
    elif status == 'ckpt':
      # get restart script downloaded and
      # restart the app from ckpt
      dmtcp.restart(src_ip, dst_ip, str(port+1), job_id)





