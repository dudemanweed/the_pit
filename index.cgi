#!/usr/bin/perl


# Remove if you're not using OpenBSD.

use OpenBSD::Unveil;
use OpenBSD::Pledge;
use POSIX qw(strftime);
use Date::Parse;
use Text::MultiMarkdown 'markdown';
my $q = new CGI;

# =====================CONFIG======================

my $ROOT = "/blog/";

# =====================END CONFIG==================

my $url = $ENV{REQUEST_URI};

sub read_file($$$);

# Remove if you're not using OpenBSD.
unveil(".","r");
pledge("rpath");

use CGI;

print $q->header(
			  -type       => 'text/html',
			  -charset    => 'utf-8',
			 );

my @entries = reverse glob("*.txt"); # Get all entries

$url =~ s/index\.cgi//;
$url =~ s/blog\.cgi//;
if ($url eq "/blog") {
	$url .= "/";
}
read_file("header.html","Index",0) if $url eq $ROOT;
read_file("notes.html","",0) if $url eq "/blog/";
my $date;
if ($url eq $ROOT || $url eq "/blog") {
	print "<ul>\n";
	foreach my $link (@entries) {
		$link =~ s/\.txt//;
		$date = str2time($link);
		my $date_string = strftime("%B %d",localtime($date));
		print "<li>$date_string: <a href=\"".$url . $link ."\">".get_title($link . ".txt") . "</a></li>\n";
	}
	print "</ul>\n";
} else {
	my $file = $url;
	$file =~ s/\/blog\///;
	if (!-e $file . ".txt") {
		read_file("header.html","404",0);
		print "<h2>That's a 404</h2>";
		print "<a href=\"./blog/index.cgi\">Go back to the index?</a>";
	} else {
		read_file("header.html",get_title($file . ".txt"), 0);
		read_file($file . ".txt","",  1);
	}
}
read_file("footer.html","",0);

sub read_file($$$) {
	my ($file, $title, $markdown) = @_;
	my $printable;
	my @contents;
	open(my $fh, "<$file");
     while (<$fh>) {
		$printable = $_;
		$printable =~ s/\[\[TITLE\]\]/$title/;
		push @contents, $printable;
	}
	if($markdown) {
		print markdown(join('', @contents));
	} else {
		print @contents;
	}
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
