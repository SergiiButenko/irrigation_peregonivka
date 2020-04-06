cd /var/www/
git reset --hard
git checkout master
git pull github master
msg=`git log -1 --pretty=%B | tr -s ' ' | tr ' ' '_'`

cd /var/www/services
cp -uv * /etc/systemd/system/
systemctl daemon-reload

echo 'systemctl restart irrigation_*'
systemctl restart irrigation_*

cd /var/www/ngnix
cp -uv * /etc/nginx/sites-available
cp -uv * /etc/nginx/sites-enabled
nginx -s reload

echo 'HEAD is now '$msg