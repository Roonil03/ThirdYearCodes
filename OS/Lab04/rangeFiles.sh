#!/usr/bin/env bash
read -r -p "Start year (e.g., 2014): " y1
read -r -p "End   year (e.g., 2015): " y2
(( y2 < y1 )) && { echo "End year must be ≥ start year"; exit 1; }
find . -type f \
  -newermt "01 Jan $y1" ! -newermt "01 Jan $((y2+1))" \
  -printf '%TY-%Tm-%Td  %p\n'
