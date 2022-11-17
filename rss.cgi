#!/usr/bin/perl

use CGI;
use POSIX qw(strftime);
use Text::MultiMarkdown 'markdown';
use v5.32;
my $q = new CGI;

use experimental 'signatures';

print "Content-Type: application/rss+xml\n\n";

# Header

print <<HERE;
<rss version="2.0">
<channel>
<title>SURAGU</title>
<link>https://suragu/blog</link>
<description>Allah I thank, my mind went blank</description>
HERE

# Only show the latest 4 posts
my $limit = 4;
my $i = 0;
foreach my $filename (reverse glob("*.txt")) {
	print "<item>\n";
	print "<title>"; print get_title($filename); print "</title>\n";
	print "<date>\n"; print get_date($filename); print "</date>\n";
	print "<link>\nhttp://$ENV{HTTP_HOST}/blog/$filename\n</link>\n";
	print "<description>\n";
	print_file($filename);
	print "</description>\n";
	print "</item>\n";
	last if $limit == ++$i;
}

print <<EOF;
</channel>
</rss>
EOF

sub print_file($file) {
	open my $fh, "<$file";
	my @file;
	while (<$fh>) {
		#$_ .= "&lt;br&gt;";
		push @file, $_;
	}
	close $fh;
	print markdown(join('', @file));

}

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
