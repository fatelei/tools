#!/bin/bash

#处理json格式的日志文件

TARGET_DIR=$1

for i in `ls $TARGET_DIR`;
do
    if [ -d $TARGET_DIR/$i ];then
        for j in `ls $TARGET_DIR/$i`;
        do
            if [ -f $TARGET_DIR/$i/$j ];then
                result=`grep 'utm_medium=email&' $TARGET_DIR/$i/$j`
                if [ ${#result} -gt 0 ];then
                    echo "${result}" >> $i
                fi
            fi
        done
    fi
done