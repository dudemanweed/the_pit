#!/usr/bin/perl

use CGI;
use POSIX qw(strftime);
my $q = new CGI;

print "Content-Type: application/rss+xml\n\n";

# Header

print <<HERE;
<rss version="2.0">
<channel>
<title>SURAGU</title>
<link>https://suragu/blog</link>
<description>Allah I thank, my mind went blank</description>
HERE

# Prototypes

sub get_title($);
sub get_title($);
sub get_date($);
sub print_file($);

# Only show the latest 4 posts
my $limit = 4;
my $i = 0;
foreach my $filename (reverse glob("*.txt")) {
	print "<item>\n";
	print "<title>"; print get_title($filename); print "</title>\n";
	print "<date>\n"; print get_date($filename); print "</date>\n";
	print "<link>\nhttp://$ENV{HTTP_HOST}/blog/$_\n</link>\n";
	print "<description>";
	print print_file($filename);
	print "</description>";
	print "</item>\n";
	last if $limit == ++$i;
	
}

print <<EOF;
</channel>
</rss>
EOF

sub print_file($) {

	my $file = shift;
	open $fh, "<$file";
	my @file;
	while (<$fh>) {
		chomp($_);
		$_ .= "&lt;br&gt;";
		push @file, $_;
	}
	print @file;
}

sub get_date($) {
	my $filename = shift;
	my @stat_thing = stat($filename);
	my $date = $stat_thing[9];
	return strftime ("%a %b %e %H:%M:%S %Y", localtime($date)) . "\n";
}

sub file_to_arr($) {
	my $file = shift;
	open $fh, "<$file";
	my @file;
	while (<$fh>) {
		push @file, $_;
	}
	return @file;
}

sub get_title($) {
	my $file = shift;
	my @file = file_to_arr($file);
	my $line = $file[0];
	$line =~ s/^\s*(.*?)\s*$/$1/;
	return $line;
}
