#!/bin/bash
python users_dump.py | tail -200  | awk -F"," '{print $2}' | sort -n | sed 's/\.[0-9]*\.[0-9]*$//' | uniq -c | sort -n | tail -10
echo "-------------------------------------------------"
python users_dump.py | tail -2000  | awk -F"," '{print $2}' | sort -n | sed 's/\.[0-9]*\.[0-9]*$//' | uniq -c | sort -n | tail -10
#echo "-------------------------------------------------"
#python dump_users.py | tail -20000  | awk -F"," '{print $2}' | sort -n | sed 's/\.[0-9]*\.[0-9]*$//' | uniq -c | sort -n | tail -10
