#!/usr/bin/bash

binDir=$(dirname $(readlink -f $0))
workDir="$binDir/.."
dataDir="$workDir/data"
tmpDir="$workDir/tmp"
resultsDir="$workDir/results"


$binDir/prepare.sh


$binDir/identify-missing-gemeindenummern.sh


$binDir/compute-pollution-by-kanton.pl  "$tmpDir/Bevoelkerung-nach-Gemeindenummer.txt" "$tmpDir/mapping-Kanton-Gemeindenummer-PLZ.txt" "$resultsDir/pollution-by-kanton.json"  2>"$resultsDir/compute-pollution-by-kanton.log"  >"$resultsDir/pollution-by-kanton.txt"

