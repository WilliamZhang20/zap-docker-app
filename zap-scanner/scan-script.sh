#!/bin/bash

path="/zap/targets"
file_path="/zap/targets/website-link.txt"

cd /

while [ ! -f $file_path ]; do
    sleep 1
done

WEBSITE_LINK=$(cat "${file_path}")

echo "Link received, ${WEBSITE_LINK}"

FILE_NAME="my_zap_report.html"

echo "Running scan..."

rm -f ${file_path}

zap-full-scan.py -t "${WEBSITE_LINK}" -r /zap/wrk/"${FILE_NAME}"