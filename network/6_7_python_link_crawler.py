#!/usr/bin/env python

import argparse
import sys
import httplib
import re

processed = []

def search_links(url, depth, search):
	# Process http links that are not processed yet
	url_is_processed = (url in processed)
	if (url.startswith("http://") and (not url_is_processed)):
		processed.append(url)
		url = host = url.replace("http://","",1)
		path = "/"


		urlparts = url.split("/")
		if (len(urlparts) > 0):
			host = urlparts[0]
			path = url.replace(host,"",1)

		#Start crawing
		print "Crawing URL path: %s%s" %(host,path)
		conn = httplib.HTTPConnection(host)
		req = conn.request("GET",path)
		results= conn.getresponse()

		#Find the links
		contents = results.read()
		all_links = re.findall('href="(.*?)"',contents)

		if (search in contents):
			print "Found " + search + " at" + url

		print " ==> %s: processing %s links " %(str(depth), str(len(all_links)))
		for href in all_links:	
			#Find relative urls
			if (href.startswith("/")):
				href = "http://" + host + href

			#Recurse links
			if (depth > 0):
				search_links(href, depth-1, search)
	else:
		print "Skiping link: %s ..." %url 


if __name__ == '__main__':
	parse = argparse.ArgumentParser(description='WebPage link crawler')
	parse.add_argument('--url', action="store", dest="url", required=True)
	parse.add_argument('--query', action="store", dest="query", required=True)
	parse.add_argument('--depth', action="store", dest="depth", default=2)
	
	given_args = parse.parse_args()

	try:
		search_links(given_args.url, given_args.depth, given_args.query)
	except KeyboardInterrupt:
		print "Aborting search by user request..."
	
