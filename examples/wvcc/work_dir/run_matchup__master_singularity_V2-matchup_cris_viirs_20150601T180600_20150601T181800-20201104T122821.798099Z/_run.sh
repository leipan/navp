#!/bin/bash

#MODULE_VERSION_STACK=3.2.10
#MANPATH=/nasa/pkgsrc/sles12/2016Q4/man:/usr/man:/usr/local/man:/man/
#HOSTNAME=hfe1
#SHELL=/bin/bash
#TERM=screen-256color
#VERDI_DIR=/home1/lpan/verdi
#SSH_CLIENT=198.9.4.11 42142 22
#HYSDS_CELERY_CFG=/home1/lpan/verdi/ops/hysds/wvcc_celeryconfig.py
#OLDPWD=/home1/lpan/pbs/wvcc
#SSH_TTY=/dev/pts/0
#USER=lpan
#HYSDS_ROOT_WORK_DIR=/nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/work/
#ENV=/usr/local/lib/init/global.kshrc
#PYTHONWARNINGS=ignore
#OSCAR_HOME=/opt/oscar
#VIRTUAL_ENV=/home1/lpan/verdi
#SANDBOX_DIR=/nobackupp12/lpan/PGE/container/container-leipan_matchup_pge_master-2020-09-15-11fefa3882d6.simg
#PATH=/nasa/singularity/3.6.4/bin:/home1/lpan/local/dmtcp2_6/bin:/home1/lpan/github/job_worker-singularity/:/home1/lpan/github/rabbitmq-utils/:/home1/lpan/verdi/bin:/home1/lpan/conda/bin:/nasa/pkgsrc/sles12/2016Q4/bin:/nasa/pkgsrc/sles12/2016Q4/sbin:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/X11R6/bin:/PBS/bin:/usr/sbin:/sbin:/opt/c3/bin:/opt/sgi/sbin:/opt/sgi/bin:/home1/lpan/bin:/bin/:/nasa/singularity/3.2.0/bin
#MAIL=/var/mail/lpan
#MODULE_VERSION=3.2.10
#PWD=/nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/work
#_LMFILES_=/nasa/modulefiles/pkgsrc/sles12/pkgsrc/2016Q4:/nasa/modulefiles/testing/singularity/3.6.4
#LANG=C
#MODULEPATH=/nasa/modulefiles/testing:/usr/share/modules/modulefiles:/nasa/modulefiles/sles12:/nasa/modulefiles/pkgsrc/sles12:/nasa/modulefiles/spack/gcc-4.8
#PYTHONSTARTUP=/etc/pythonstart
#TZ=PST8PDT
#LOADEDMODULES=pkgsrc/2016Q4:singularity/3.6.4
#NOBACKUP=/nobackupp12/lpan/wvcc
#C3_RSH=ssh -oConnectTimeout=10 -oForwardX11=no
#PBS_JOBID=1666
#HOME=/home1/lpan
#SHLVL=2
#PKGSRC_BASE=/nasa/pkgsrc/sles12/2016Q4
#HYSDS_ROOT_CACHE_DIR=/nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/cache
#HYSDS_DATASETS_CFG=/home1/lpan/verdi/etc/wvcc_config/datasets.json
#HYSDS_CELERY_CFG_MODULE=wvcc_celeryconfig
#LOGNAME=lpan
#SYSTEMD_LESS=-FRXMK
#CVS_RSH=ssh
#SSH_CONNECTION=198.9.4.11 42142 129.99.230.70 22
#MODULESHOME=/usr/share/Modules/3.2.10
#OMP_NUM_THREADS=28
#INFOPATH=/nasa/pkgsrc/sles12/2016Q4/info
#DISPLAY=hfe1:30.0
#BASH_FUNC_module%%=() {  eval `/usr/bin/modulecmd bash "$@"`
}
#_=/home1/lpan/verdi/bin/celery
#LC_CTYPE=C.UTF-8
#_MP_FORK_LOGLEVEL_=20
#_MP_FORK_LOGFILE_=
#_MP_FORK_LOGFORMAT_=[%(asctime)s: %(levelname)s/%(processName)s] %(message)s
#CELERY_LOG_LEVEL=20
#CELERY_LOG_FILE=
#CELERY_LOG_REDIRECT=1
#CELERY_LOG_REDIRECT_LEVEL=WARNING


singularity exec --userns --no-home --home /home/ops --bind /nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/work/jobs:/nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/work/jobs --bind /nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/work/tasks:/nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/work/tasks --bind /nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/work/workers:/nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/work/workers --bind /nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/cache/cache:/nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/cache/cache:ro --bind /home1/lpan/.netrc:/home/ops/.netrc:ro --bind /home1/lpan/.aws:/home/ops/.aws:ro --bind /home1/lpan/verdi/etc/wvcc_settings.conf:/home/ops/wvcc/conf/settings.conf:ro --bind /home1/lpan/verdi/ops/hysds/wvcc_celeryconfig.py:/wvcc_celeryconfig.py:ro --bind /home1/lpan/verdi/etc/wvcc_config/datasets.json:/datasets.json:ro --pwd /nobackupp12/lpan/wvcc/worker/2020/11/04/20201104T044007-pleiades_worker.1666/work/jobs/2020/11/04/12/40/run_matchup__master_singularity_V2-matchup_cris_viirs_20150601T180600_20150601T181800-20201104T122821.798099Z /nobackupp12/lpan/PGE/container/container-leipan_matchup_pge_master-2020-09-15-11fefa3882d6.simg /home/ops/matchup_pge/run_matchup.sh 20150601T201500 20150601T205500
