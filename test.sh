#!/bin/bash

if [ $# -ge 0 ]; then
    num=$#
    for i in 0..$num; do
        echo "$i"
    done
fi

