#! /bin/bash
set -x
print 'start training......'
#source /root/.bashrc

#ps -ef|grep python |grep -v grep | awk '{print $2}'|xargs kill -9

pkill -9 gunicorn
pkill -9 python

sleep 1

#!!!!!!!!!delete news!!!!!!!######
rm -rf /home/workspace/lsi/viva.index
rm -rf /home/workspace/lsi/viva.index.0
rm -rf /home/workspace/lsi/viva.lsi
rm -rf /home/workspace/lsi/viva.lsi.projection
rm -rf /home/workspace/lsi/viva.mm
rm -rf /home/workspace/lsi/viva_temp.mm
rm -rf /home/workspace/lsi/viva_temp.mm.index

cp /home/workspace/lsitemp/* /home/workspace/lsi/

sleep 1
#gunicorn -w4 -t 240 -k gevent -b0.0.0.0:3000 service_viva:app --preload --limit-request-line 0
gunicorn -w4 -t 600 -k gevent -b0.0.0.0:3000 service_viva:app --preload --limit-request-line 0 --worker-connections 500



