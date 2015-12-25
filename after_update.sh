#! /bin/bash
set -x
print 'start training......'
#source /root/.bashrc
#mv /home/workspace/news /home/workspace/bak/article/news_`date -d now +%Y%m%

# workspace = baobao/Documents/LSI-for-ChineseDocument


#ps -ef|grep python |grep -v grep | awk '{print $2}'|xargs kill -9

pkill -9 gunicorn
pkill -9 python

sleep 1

#!!!!!!!!!delete news!!!!!!!######
rm -rf /home/baobao/Documents/LSI-for-ChineseDocument/lsi/viva.index
rm -rf /home/baobao/Documents/LSI-for-ChineseDocument/lsi/viva.index.0
rm -rf /home/baobao/Documents/LSI-for-ChineseDocument/lsi/viva.lsi
rm -rf /home/baobao/Documents/LSI-for-ChineseDocument/lsi/viva.lsi.projection
rm -rf /home/baobao/Documents/LSI-for-ChineseDocument/lsi/viva.mm
rm -rf /home/baobao/Documents/LSI-for-ChineseDocument/lsi/viva_temp.mm
rm -rf /home/baobao/Documents/LSI-for-ChineseDocument/lsi/viva_temp.mm.index

cp /home/baobao/Documents/LSI-for-ChineseDocument/lsitemp/* /home/baobao/Documents/LSI-for-ChineseDocument/lsi/

sleep 1
#gunicorn -w4 -t 240 -k gevent -b0.0.0.0:3000 service_viva:app --preload --limit-request-line 0
gunicorn -w4 -t 600 -k gevent -b0.0.0.0:3000 service_viva:app --preload --limit-request-line 0 --worker-connections 500



