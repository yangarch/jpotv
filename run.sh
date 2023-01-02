PID=`ps -ef | grep jpotv_discord.py | awk '{print $2}'`

for i in $PID
do
    echo $i
    kill -9 $i
done

nohup python3 script/njc_discord.py > /tmp/logs/discord_log.txt &