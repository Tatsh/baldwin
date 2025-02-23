#!/usr/bin/env bash
set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)/.."
YEAR=$(date +%Y)
MONTH_DATE=$(date +%m-%d)

sed -re "s/^local date_released = .*/local date_released = '%s-$MONTH_DATE' % copyright_year;/" \
    -i "${PROJECT_DIR}/.project.jsonnet"
sed -re "s/^Copyright \(c\) [0-9]+/Copyright \(c\) ${YEAR}/" -i "${PROJECT_DIR}/LICENSE.txt"
sed -re "s/date-released: .*/date-released: '${YEAR}-${MONTH_DATE}'/" \
    -i "${PROJECT_DIR}/CITATION.cff"
for i in "${PROJECT_DIR}/man/"*.1; do
    sed -re "s/^20[0-9][0-9]$/${YEAR}/" -i "${i}"
done
