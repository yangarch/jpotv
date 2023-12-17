sh proxy_run.sh 로 프록시를 띄워 준 후에
크론으로 돌려야 함.

0 8 * * 1 /usr/bin/python3 /Users/archmacmini/Project/lunchbot/get_todays_lunch.py >> /Users/archmacmini/tmp/logs/lunchbot_log.txt
10,25,40,55 * * * * /Users/archmacmini/3.9/bin/python /Users/archmacmini/Project/jpotv/proxy/jpotv_web.py
