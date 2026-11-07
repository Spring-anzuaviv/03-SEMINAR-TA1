#!/usr/bin/env bash
set -e
base=http://localhost:5080
curl -s "$base/"; echo
future=$(date -d '+30 days' +%F 2>/dev/null || date -v+30d +%F)
body="{"customerName":"ABC Logistics","effectiveDate":"$future"}"
echo 'Create:'; curl -s -i -X POST "$base/api/contracts" -H 'Content-Type: application/json' -d "$body"; echo
# Demo assumes first new contract ID=1 after a fresh server start
echo 'Submit ID 1:'; curl -s -i -X POST "$base/api/contracts/1/submit"; echo
echo 'Repeat submit ID 1:'; curl -s -i -X POST "$base/api/contracts/1/submit"; echo
