#!/bin/bash

path="/zap/targets"
file_path="/zap/targets/website-link.txt"

cd /

while [ ! -f $file_path ]; do
    sleep 1
done

WEBSITE_LINK=$(cat "${file_path}")

TIME_LIMIT=$(cat "${path}"/time-limit.txt)

echo "Link received, ${WEBSITE_LINK}"

CURR_DATE=$(date +"%Y-%b-%d_%H-%M-%S")

FILE_NAME="${CURR_DATE}_zap_report"

echo "Going for ${TIME_LIMIT} minute time limit"

rm -f $file_path

echo "Running scan..."

zap-full-scan.py -t "${WEBSITE_LINK}" -m ${TIME_LIMIT} -r /zap/wrk/"${FILE_NAME}".html