#!/bin/sh

CR_TIME=`echo $(($(date +%s%N)/1000000))`
find /var/www/app/web/templates -type f -print0 | xargs -0 sed -i 's/JS_VERSION/'$CR_TIME'/g'