# jpotv
searching jpotv live channel

run.sh 하기 전에 환경변수 import를 위해 . ~/.bash_profile 해야함


flask를 gunicorn으로 띄우기

gunicorn -w 4 -b 0.0.0.0:8000 app:app


----
 1730  systemctl stop dockedr
 1731  systemctl stop docker
 1732  systemctl stop docker.socket
 1733  umount docker
 1734  fdisk -l
 1735  mount /dev/sdd1 /home/docker
 1736  systemctl start docker
 1737  docker start fastapi_test
