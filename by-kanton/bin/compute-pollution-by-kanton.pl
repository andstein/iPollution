#!/usr/bin/perl

use warnings;
use strict;
use FindBin qw($Bin);


#my $wd = $Bin;		# working dir
#my $Bev_nach_GDENR_FILE = "$wd/Bevoelkerung-nach-Gemeindenummer.txt";
#my $mapping_FILE = "$wd/mapping-Kanton-Gemeindenummer-PLZ.txt";
#my $JSON_results_FILE = "$wd/pollution-by-kanton.json"


die "usage: $0 FILE1 FILE2 FILE3"
	unless (@ARGV == 3);
(my $Bev_nach_GDENR_FILE, my $mapping_FILE, my $JSON_results_FILE) = @ARGV;



my $webService = "http://127.0.0.1:5000/values?plz=";

my @timerange = (1990 .. 2007);
my @schadstoffe = ("o3", "pm10", "no2");

my $precision = 2;

my $DELIM = "========================================";


my %Bev = ();
my %GDENRn_of_Kanton = ();	# hash of arrays
my %PLZen_of_GDENR = ();	# hash of arrays

my @kanton_JSON_pairs = ();	# to record info for overall output object




my $JSON_TESTDATA = '{"o3": {"1992": 150, "1993": 150, "1994": 150, "1998": 150, "1999": 150, "2000": 150, "2004": 250, "2005": 250, "2006": 250}, "pm10": {"1998": 22.5, "1999": 22.5, "2000": 22.5, "2001": 22.5, "2002": 22.5, "2003": 32.5, "2004": 22.5, "2005": 22.5, "2006": 22.5, "2007": 17.5}, "no2": {"1990": 12.5, "1991": 12.5, "1992": 42.5, "1993": 27.5, "1994": 27.5, "1995": 27.5, "1996": 27.5, "1997": 27.5, "1998": 27.5, "1999": 27.5, "2000": 27.5, "2001": 22.5, "2002": 22.5, "2003": 27.5, "2004": 22.5, "2005": 22.5, "2006": 22.5, "2007": 22.5}}';

my $JSON_TESTDATA2 = '{"o3": {"1992": 99, "1993": 150, "1994": 150, "1998": 150, "1999": 150, "2000": 150, "2004": 250, "2005": 250, "2006": 250}, "pm10": {"1998": 22.5, "1999": 22.5, "2000": 22.5, "2001": 22.5, "2002": 22.5, "2003": 32.5, "2004": 22.5, "2005": 22.5, "2006": 22.5, "2007": 17.5}, "no2": {"1990": 12.5, "1991": 12.5, "1992": 42.5, "1993": 27.5, "1994": 27.5, "1995": 27.5, "1996": 27.5, "1997": 27.5, "1998": 27.5, "1999": 27.5, "2000": 27.5, "2001": 22.5, "2002": 22.5, "2003": 27.5, "2004": 22.5, "2005": 22.5, "2006": 22.5, "2007": 22.5}}';


my %TESTDATA = (
	o3 => { 
		"1992" => 150,
		"1993" => 150,
		"1994" => 150,
		"1998" => 150,
		"1999" => 150,
		"2000" => 150,
		"2004" => 250,
		"2005" => 250,
		"2006" => 250
	},
	pm10 => {
		"1998" => 22.5,
		"1999" => 22.5,
		"2000" => 22.5,
		"2001" => 22.5,
		"2002" => 22.5,
		"2003" => 32.5,
		"2004" => 22.5,
		"2005" => 22.5,
		"2006" => 22.5,
		"2007" => 17.5
	},
	no2 => {
		"1990" => 12.5,
		"1991" => 12.5,
		"1992" => 42.5,
		"1993" => 27.5,
		"1994" => 27.5,
		"1995" => 27.5,
		"1996" => 27.5,
		"1997" => 27.5,
		"1998" => 27.5,
		"1999" => 27.5,
		"2000" => 27.5,
		"2001" => 22.5,
		"2002" => 22.5,
		"2003" => 27.5,
		"2004" => 22.5,
		"2005" => 22.5,
		"2006" => 22.5,
		"2007" => 22.5
	}
);




# SUBS
#########################################################

sub contains ( $ $ ) {
	my @array = @{ shift @_ };
	my $value = shift @_ ;
	
	for my $elem (@array) {
		return 1
			if ($elem eq $value);
	}
	
	return 0;
}

sub print_pollution_hash ( $ ) {
	my %pollution_hash = %{ shift @_ };
	for my $stoff (@schadstoffe) {
		for my $year (@timerange) {
			if (exists $pollution_hash{$stoff}{$year}) {
				print "$stoff | $year :  $pollution_hash{$stoff}{$year}\n";
			}
		}
	}	
}

sub print_pollution_hash_tabular ( $ ) {
	my %pollution_hash = %{ shift @_ };
	$" = "\t";  	# dummy to recover syntax highlighting: "
	print " \t@schadstoffe\n";
	for my $year (@timerange) {
		my @vals = ();
		for my $stoff (@schadstoffe) {
			push @vals,
				((exists $pollution_hash{$stoff}{$year}) ?(sprintf "%.${precision}f", $pollution_hash{$stoff}{$year}) :"NA");
		}
		print "$year\t@vals\n";
	}	
}

sub JSON_scraper ( $ ) {
	my $orig_obj = shift;
	my %pollution_hash = ();
	for my $stoff (@schadstoffe) {
		if ($orig_obj =~ m@"$stoff": *(\{[^{}]*)\}@) {
			my $stoff_obj = $1;
			for my $year (@timerange) {
				if ($stoff_obj =~ m@"$year": *([0-9.]+)@) {
					$pollution_hash{$stoff}{$year} = $1;
#					print "$stoff|$year: $1\n";
				}
			}
		}
	}
	return %pollution_hash;	
}


sub JSON_constructor_from_pair_strings ( $ ) {
	my @pair_strings = @{ shift @_ };
	return ("{" . (join ", ", @pair_strings) ."}");
}


sub JSON_constructor_kanton ( $ ) {
	my %pollution_hash = %{ shift @_ };
	my @stoff_obj_pairs = ();
	for my $stoff (@schadstoffe) {
		my @year_val_pairs = ();
		for my $year (@timerange) {
			if (exists $pollution_hash{$stoff}{$year}) {
				push @year_val_pairs, "\"$year\": $pollution_hash{$stoff}{$year}";
			}
		}
		if (scalar(@year_val_pairs) > 0) {
			push @stoff_obj_pairs, ("\"$stoff\": " . JSON_constructor_from_pair_strings(\@year_val_pairs));
		}
	}
	return JSON_constructor_from_pair_strings(\@stoff_obj_pairs);
}




#my %poll_hash = JSON_scraper($JSON_TESTDATA);
#print_pollution_hash_tabular(\%poll_hash);
#print_pollution_hash_tabular(\%TESTDATA);
#my $JSON_RECONSTRUCTED = JSON_constructor_kanton(\%poll_hash);
#print "orig:          $JSON_TESTDATA\n";
#print "reconstructed: $JSON_RECONSTRUCTED\n";
#if ($JSON_TESTDATA ne $JSON_RECONSTRUCTED) {print "reconstruciton failed\n"} else {print "reconstruciton successful\n"}
#exit;


#my $curr_PLZ = "8001";
#$curr_PLZ = "4051";
#my $URL="$webService$curr_PLZ";
#my $json_response = `wget -O - "$URL"`;
#my %poll_hash = JSON_scraper($json_response);
#print "response: '$json_response'\n";
#print_pollution_hash_tabular(\%poll_hash);
#exit;




# Bevölkerungsgrösse pro Gemeinde im RAM speichern
#########################################################

open BEV_INFILE, "<$Bev_nach_GDENR_FILE"
	or die "cannot open '$Bev_nach_GDENR_FILE' for reading: $!";

while (my $line = <BEV_INFILE>) {
	$line =~ s/\s+$//;
	(my $GDENR, my $Bev_size) = split /\s+/, $line;
	$Bev{$GDENR} = $Bev_size;
}
close BEV_INFILE;





# Mapping-Info im RAM speichern
#########################################################

open MAP_INFILE, "<$mapping_FILE"
	or die "cannot open '$mapping_FILE' for reading: $!";

MAP_LINE:
while (my $line = <MAP_INFILE>) {
	$line =~ s/\s+$//;
#	print "$line\n";
	(my $kanton, my $GDENR, my $PLZ) = split /\s/, $line;
#	print "$kanton, $GDENR, $PLZ\n";

	unless (exists $Bev{$GDENR}) {
		print STDERR "WARNING: Kanton '$kanton' is associated with Gemeindenummer '$GDENR' the population size of which is unknown. (PLZ: $PLZ). Proceeding anyway. This Gemeindenummer will be ignored.\n";
		next MAP_LINE;
	}
	unless (contains(\@{ $GDENRn_of_Kanton{$kanton} }, $GDENR)) {
		push @{ $GDENRn_of_Kanton{$kanton} }, $GDENR;
	}
	push @{ $PLZen_of_GDENR{$GDENR} }, $PLZ;
}

close MAP_INFILE;


# TODO: test collapsing of duplicate entries in GDERN_of_Kanton



# Reihenfolge der Kantone aus dem mapping-File extrahieren
###########################################################
$_ = `cat $mapping_FILE | cut -f1 | uniq`;
my @kantone = split /\s+/, $_;




# Kantone der Reihe nach abarbeiten
#########################################################


#print STDERR "kantone (", scalar(@kantone), "): @kantone\n\n";
#@_ = (keys %GDENRn_of_Kanton);
#print STDERR "kantone2 (", scalar(@_), "): @_\n";
#exit;

#KANTONE-LOOP:
for my $curr_kanton (@kantone) {

	print STDERR "\n\n$DELIM\nprocessing Kanton $curr_kanton\n$DELIM\n";
#	print STDERR "arrayRef: $GDENRn_of_Kanton{$curr_kanton}\n";
	my @GDENRn = @{ $GDENRn_of_Kanton{$curr_kanton} };

	my %pollution_for_curr_kanton = ();
	my %population_sum_for_curr_kanton = ();

#	GDENR_LOOP:
	for my $curr_GDENR (@GDENRn) {
		
		my @PLZen = @{ $PLZen_of_GDENR{$curr_GDENR} };

		my %pollution_for_curr_GDENR = ();
		my %val_ctr_for_curr_GDENR = ();
		
		PLZ_LOOP:
		for my $curr_PLZ (@PLZen) {

			print STDERR "\n$DELIM\nprocessing PLZ $curr_PLZ\n";
			
			my $URL="$webService$curr_PLZ";
			my $response_JSON = `wget -O - "$URL"`;
			if ($response_JSON =~ "error") {
				print STDERR "WARNING: PLZ '$curr_PLZ' is not known by the pollution webservice (Kanton/GDENR: $curr_kanton/$curr_GDENR). Proceeding anyway. This PLZ will be ignored.\n";
				next PLZ_LOOP;
			}
			my %pollution_for_curr_PLZ = JSON_scraper($response_JSON);

#			my %pollution_for_curr_PLZ = JSON_scraper($JSON_TESTDATA);
#			%pollution_for_curr_PLZ = JSON_scraper($JSON_TESTDATA2)
#				if $curr_PLZ==8051;
#			my %pollution_for_curr_PLZ = %TESTDATA;
#			print "\nPLZ: $curr_PLZ\n";
#			print_pollution_hash_tabular(\%pollution_for_curr_PLZ);
			
			# record these values in %pollution_for_curr_GDENR
			# and increment the value counter, so we can later derive the mean values for the current GDENR
			for my $stoff (@schadstoffe) {
				for my $year (@timerange) {
					if (exists $pollution_for_curr_PLZ{$stoff}{$year}) {
						$pollution_for_curr_GDENR{$stoff}{$year} += $pollution_for_curr_PLZ{$stoff}{$year};
						$val_ctr_for_curr_GDENR{$stoff}{$year}++;
					}
				}
			}
		}
		
		# derive the mean pollution values for the current GDENR
		for my $stoff (@schadstoffe) {
			for my $year (@timerange) {
				if ((exists $val_ctr_for_curr_GDENR{$stoff}{$year}) && ($val_ctr_for_curr_GDENR{$stoff}{$year} > 0)) {
					$pollution_for_curr_GDENR{$stoff}{$year} *= (1 / $val_ctr_for_curr_GDENR{$stoff}{$year});
				}
			}
		}
#		print "\nGDENR: $curr_GDENR\n";
#		print_pollution_hash_tabular(\%pollution_for_curr_GDENR);

		# record these values in %pollution_for_curr_kanton (weighted by the population size)
		# and update the population sum, so we can later derive the weighted values for the current kanton
		for my $stoff (@schadstoffe) {
			for my $year (@timerange) {
				if (exists $pollution_for_curr_GDENR{$stoff}{$year}) {
					$pollution_for_curr_kanton{$stoff}{$year} += $Bev{$curr_GDENR} * $pollution_for_curr_GDENR{$stoff}{$year};
					$population_sum_for_curr_kanton{$stoff}{$year} += $Bev{$curr_GDENR};
				}
			}
		}
		
		
	}

	# derive the weighted pollution values for the current kanton
	for my $stoff (@schadstoffe) {
		for my $year (@timerange) {
			if ((exists $population_sum_for_curr_kanton{$stoff}{$year}) && ($population_sum_for_curr_kanton{$stoff}{$year} > 0)) {
				$pollution_for_curr_kanton{$stoff}{$year} *= (1 / $population_sum_for_curr_kanton{$stoff}{$year});
			}
		}
	}


	# print results for current kanton
	print "\n$DELIM\nKanton: $curr_kanton\n$DELIM\n";
	print_pollution_hash_tabular(\%pollution_for_curr_kanton);
#	my %poll_hash = JSON_scraper($JSON_TESTDATA);
#	print_pollution_hash_tabular(\%poll_hash);
#	%poll_hash = JSON_scraper($JSON_TESTDATA2);
#	print_pollution_hash_tabular(\%poll_hash);
#	exit;
	
	# store a pair (kanton, JSON obj.) as string for this kanton
	push @kanton_JSON_pairs, ("\"$curr_kanton\": " . JSON_constructor_kanton(\%pollution_for_curr_kanton));
	
}


#print "\nTEST:\n";
#my %poll_hash = JSON_scraper($JSON_TESTDATA);
#print_pollution_hash(\%poll_hash);
#print_pollution_hash_tabular(\%poll_hash);
#print_pollution_hash(\%TESTDATA);



# write full results as JSON object to file
#########################################################
open JSON_OUTFILE, ">$JSON_results_FILE"
	or die "cannot open '$JSON_results_FILE' for writing: $!";
print JSON_OUTFILE JSON_constructor_from_pair_strings(\@kanton_JSON_pairs), "\n";
close JSON_OUTFILE
