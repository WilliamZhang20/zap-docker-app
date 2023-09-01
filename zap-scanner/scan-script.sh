#!/bin/bash

path="/zap/targets"
file_path="/zap/targets/website-link.txt"

cd /

while [ ! -f $file_path ]; do
    sleep 1
done

WEBSITE_LINK=$(cat "${file_path}")

echo "Link received, ${WEBSITE_LINK}"

CURR_DATE=$(date +"%Y-%b-%d_%H-%M-%S")

FILE_NAME="${CURR_DATE}_zap_report"

echo "Running scan..."

rm -f ${file_path}

echo "${FILE_NAME}.html" > "${path}"/file_name.txt

zap-full-scan.py -t "${WEBSITE_LINK}" -r /zap/wrk/"${FILE_NAME}".