PID=`ps -ef | grep jpotv_proxy.py | awk '{print $2}'`

for i in $PID
do
    echo $i
    kill -9 $i
done

nohup mitmdump -s jpotv_proxy.py -p 18080 >> /Users/archmacmini/Project/jpotv/logs/jpotv_proxy_log.txt &