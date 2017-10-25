#!/bin/sh

mkdir -p predictionio-setup/bin
cd predictionio-setup
curl -o bin/pio-setup https://raw.githubusercontent.com/jpioug/predictionio-setup/master/bin/pio-setup
chmod +x bin/pio-setup

PIO_GIT_USER=apache PIO_GIT_BRANCH=develop PIO_EVENTDATA_REFRESH=true ./bin/pio-setup deploy
touch target/pio-setup.log
tail -f target/pio-setup.log &

counter=1
ret=7
while [ $ret = 7 -a $counter != 10 ] ; do
  ./bin/pio-setup start
  sleep 5
  curl -v 127.0.0.1:7070/events.json
  ret=$?
  echo "Checking Java processes..."
  ps aux | grep java
  echo "Checking 7070 port..."
  netstat | grep 7070
  counter=`expr $counter + 1`
done

./bin/pio-setup status
tail -f ~/pio.log &
