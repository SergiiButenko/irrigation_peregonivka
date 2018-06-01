cd /var/www/
git reset --hard
git pull origin dev
msg=`git log -1 --pretty=%B | tr -s ' ' | tr ' ' '_'`

cd /var/www/services
cp -uv * /etc/systemd/system/

systemctl daemon-reload

systemctl restart irrigation_7543.service

echo 'HEAD is now '$msg