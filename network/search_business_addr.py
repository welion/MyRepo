#!/usr/bin/env python

from pygeocoder import Geocoder
import argparse

def search_business(business_name):
	
	results = Geocoder.geocode(business_name)

	for result in resilts:
		print result


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Business location Search')
	parser.add_argument('--name',action='store',dest='business_name',required=True)
	given_args = parser.parse_args()

	print "Searching %s" %given_args.business_name
	search_business(given_args.business_name)
	

