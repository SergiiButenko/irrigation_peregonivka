cd /var/www/
git reset --hard
git checkout master
git pull origin master
msg=`git log -1 --pretty=%B | tr -s ' ' | tr ' ' '_'`

cd /var/www/services
cp -uv * /etc/systemd/system/
systemctl daemon-reload

cd /var/www/ngnix
cp -uv * /etc/nginx/sites-available
cp -uv * /etc/nginx/sites-enabled
nginx -s reload

echo 'systemctl restart irrigation_7542.service'
systemctl restart irrigation_7542.service
echo 'systemctl restart rules_handler.service'
systemctl restart rules_handler.service
echo 'systemctl restart greenhouse_handler.service'
systemctl restart greenhouse_handler.service
echo 'systemctl restart irrigation_data_logger.service'
systemctl restart irrigation_data_logger.service
echo 'systemctl restart irrigation_telegram_bot.service'
systemctl restart irrigation_telegram_bot.service
echo 'HEAD is now '$msg