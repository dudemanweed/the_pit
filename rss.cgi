#!/usr/bin/perl

use CGI;
use POSIX qw(strftime);

my $q = new CGI;

print "Content-Type: application/rss+xml\n\n";

# Header

print <<HERE;
<rss version="2.0">
<channel>
<title>qorg's trashyard</title>
<link>https://qorg11.net/trashyard</link>
<description>whatever that comes to my mind</description>
HERE

for (reverse glob("*.txt")) {
	$_ =~ s/\.txt//;
	print "<item>\n";
	print "<title>\n$_</title>\n";
	# print "<date>\n"; print get_date($_); print "</date>\n";
	print "<link>\nhttp://$ENV{HTTP_HOST}/trashyard/$_\n</link>\n";
	print "<description>";
	print print_file($_ . ".txt");
	print "</description>";
	print "</item>\n";
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
	return @file;
}

sub get_date($) {
	my $filename = shift;
	my @stat_thing = stat($filename);
	my $date = $stat_thing[9];
	return strftime ("%a %b %e %H:%M:%S %Y", gmtime($date)) . "\n";
}
