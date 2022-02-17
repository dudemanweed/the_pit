#!/usr/bin/perl

use CGI;
my $q = new CGI;

# =====================CONFIG======================

my $ROOT = "/trashyard/";

# =====================END CONFIG==================

my $url = $ENV{REQUEST_URI};

sub read_file($);

print $q->header("application/xhtml+xml");
my @entries = reverse glob("*.txt"); # Get all entries

$url =~ s/index\.cgi//;
$url =~ s/blog\.cgi//;

read_file("header.html");
read_file("notes.html") if $url eq $ROOT;

if ($url eq $ROOT) {
	print "<ul>\n";
	foreach my $link (@entries) {
		$link =~ s/\.txt//;
		print "<li><a href=\"".$url . $link ."\">".get_title($link . ".txt") . "</a></li>\n";
	}
	print "</ul>\n";
} else {
	my $file = $url;
	$file =~ s/$ROOT//;
	if(!-e $file . ".txt") {
		print $q->h1("This is a 404...");
		print "<a href=\"./\">Go back to the index?</a>";
	} else {
		print "<pre>";
		read_file($file . ".txt");
		print "</pre>";
	}
}
read_file("footer.html");

sub read_file($) {
	my $file = shift;
	open(my $fh, "<$file");
	print while <$fh>;
	close $fh;
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
