#!/bin/sh

while true
do
	last=`wc -l jd_comment.json`
    sleep 10
    now=`wc -l jd_comment.json`
    timestamp=`date`
    echo "[$timestamp]last $last, now $now"
    if [ "X$last" == "X$now" ];then
        kill -2 `pidof python`
        kill -2 `pidof python`
        sleep 100
        nohup scrapy crawl JdComment -s JOBDIR=crawls/JdComment &
    fi
done
