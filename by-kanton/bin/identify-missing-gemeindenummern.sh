#!/usr/bin/bash

# ideally, the two resulting files gemeindenummern.*missing.*.txt should be empty
# otherwise, the coverage of mappings PLZ -> Gemeindenummer -> Kanton won't be fully treliable

# Unterschiede entstehen oft durch Zusammenschlüsse von Gemeinden (meist am 1.7.2011 erfolgt).
# Unsere Datenquellen sind leider unterschiedlich alt: Die Daten im Mapping-File scheinen neur zu sein.
# Neuere Bevölkerungsdaten haben wir aber leider nicht, deshalb passen wir Mismatches manuell im File mapping-PLZ-Kanton-Gemeindenummer-CORRECTED.txt an.


binDir=$(dirname $(readlink -f $0))
workDir="$binDir/.."
dataDir="$workDir/data"
tmpDir="$workDir/tmp"
resultsDir="$workDir/results"


cat "$dataDir/mapping-PLZ-Kanton-Gemeindenummer-CORRECTED.txt"  |  cut -f 3   |  sort -n| uniq  >"$tmpDir/gemeindenummern-acc-to-mapping.txt"

cat "$tmpDir/Bevoelkerung-nach-Gemeindenummer.txt"   |  egrep -v GDENR  |  cut -f 1  |  sort -n  |  uniq  >"$tmpDir/gemeindenummern-acc-to-bevoelkerungsstatistik.txt"



diff "$tmpDir/gemeindenummern-acc-to-mapping.txt" "$tmpDir/gemeindenummern-acc-to-bevoelkerungsstatistik.txt" -y  |  egrep -e '<'  |  perl -pe 's/\s+<\t*$//'  >"$tmpDir/gemeindenummern-acc-to-mapping-missing-in-bevoelkerungsstatistik.txt"

diff "$tmpDir/gemeindenummern-acc-to-mapping.txt" "$tmpDir/gemeindenummern-acc-to-bevoelkerungsstatistik.txt" -y  |  egrep -e '>'  |  perl -pe 's/^\s*>\s+//'  >"$tmpDir/gemeindenummern-acc-to-bevoelkerungsstatistik-missing-in-mapping.txt"

