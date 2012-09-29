#!/usr/bin/bash

binDir=$(dirname $(readlink -f $0))
workDir="$binDir/.."
dataDir="$workDir/data"
tmpDir="$workDir/tmp"
resultsDir="$workDir/results"


bevoelk_orig="$dataDir/Bevoelkerung-nach-Gemeindenummer-ORIG.txt"
bevoelk_gemeinden="$tmpDir/Bevoelkerung-nach-Gemeindenummer.txt"

mapping="$dataDir/mapping-PLZ-Kanton-Gemeindenummer-CORRECTED.txt"		# manuell korrigierte Gemeindenummern
mapping_sorted="$tmpDir/mapping-Kanton-Gemeindenummer-PLZ.txt"



# bevoelkerungszahlen-Infos aufräumen und auf relevante Daten reduzieren
cat $bevoelk_orig  |
	egrep  "^[[:space:]]*[0-9]+ "  |
	perl -ne '
		s/(\d) (\d)/$1$2/g;
		s/^\s+//;
		s/^(\d+) +/$1\t/;
		s/ *\t+ */\t/g;
		@_ = split /\t/, $_;
		$_ = join "\t", @_[0,10,1];
		print "$_\n";
	'  >$bevoelk_gemeinden


# sortiere Mapping nach Gemeindenummern und dadurch auch nach Kantonen
cat $mapping  |
	egrep -v '^PLZ'  |
	sort -k3 -n |
	perl -ne '
		s/\s+$//;
		@_ = split /\t/, $_;
		$_ = join "\t", @_[1,2,0,3];
		print "$_\n";
	'  >$mapping_sorted

