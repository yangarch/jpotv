# jpotv
searching jpotv live channel

run.sh 하기 전에 환경변수 import를 위해 . ~/.bash_profile 해야함


flask를 gunicorn으로 띄우기

gunicorn -w 4 -b 0.0.0.0:8000 app:app

crom 활성
service cron start

systemctl stop docker  
systemctl stop docker.socket  
umount docker  
fdisk -l  
mount /dev/sdd1 /home/docker  
systemctl start docker  
docker start fastapi_test  
