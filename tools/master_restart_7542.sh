cd /var/www/
find . -name '*.pyc' -delete

git reset --hard
git checkout master
git pull origin master
msg=`git log -1 --pretty=%B | tr -s ' ' | tr ' ' '_'`

cd /var/www/services
cp -uv * /etc/systemd/system/
systemctl daemon-reload

echo 'systemctl restart irrigation_docker_compose.service'
systemctl restart irrigation_docker_compose.service 
