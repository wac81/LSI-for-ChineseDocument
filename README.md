# LSI-for-ChineseDocument
LSI-for-ChineseDocument

lsimodel.py:use_svdlibc=True

service.py for lsi and other NLP


similarity_run.py  for create lsi model


pip install gunicorn   for service_viva.py 

gunicorn -w4 -t 600 -k gevent -b0.0.0.0:3000 service_viva:app --preload --limit-request-line 0 --worker-connections 500