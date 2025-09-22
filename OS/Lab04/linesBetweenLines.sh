#!/usr/bin/env bash

file=$1; start=$2; end=$3
[[ ! -f $file ]] && { echo "File not found"; exit 1; }
[[ $start -le 0 || $end -lt $start ]] && { echo "Invalid range"; exit 1; }
sed -n "${start},${end}p" "$file"
