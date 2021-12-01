#!/bin/bash
lastday=$(ls | grep -v '\.' | sort -n | tail -1)
(( new = $lastday + 1 ))
mkdir $new
cp template.py $new/day$new.py
