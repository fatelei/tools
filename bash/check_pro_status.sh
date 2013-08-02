#!/bin/bash

#用于检测服务是否是运行状态

service=$1

while true
do
    ps -a | grep -v grep | grep $1 > /dev/null
    result=$?
    if [ "${result}" -eq "0" ];then
        echo running
    else
        break
    fi
done
