#!/usr/bin/perl

package Util;
use v5.32;
use experimental 'signatures';
use Exporter;
use POSIX;
our @EXPORT_OK = qw(get_date file_to_arr get_title);
our @EXPORT = qw(get_date file_to_arr get_title);

sub get_date($filename) {
	my @stat_thing = stat($filename);
	my $date = $stat_thing[9];
	return strftime ("%a %b %e %H:%M:%S %Y", localtime($date)) . "\n";
}

sub file_to_arr($file) {
	open my $fh, "<$file";
	my @file;
	while (<$fh>) {
		push @file, $_;
	}
	return @file;
	close $fh;
}

sub get_title($file) {
	my @file = file_to_arr($file);
	my $line = $file[0];
	# Remove trailing whitespaces
	$line =~ s/^\s*(.*?)\s*$/$1/;
	return $line;
}

1;
