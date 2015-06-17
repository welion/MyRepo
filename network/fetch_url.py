#-*- coding: utf-8 -*-
#!/usr/bin/env python

import argparse
import tornado.httpclient

def fetch(url):
	http_header = {'User-Agent':'Chorme'}
	http_request = tornado.httpclient.HTTPRequest(url=url, method='GET', headers=http_header, connect_timeout=120, request_timeout=600)
	
	http_client = tornado.httpclient.HTTPClient()
	
	http_response = http_client.fetch(http_request)
	print http_response.code
	
	for field in http_response.headers.get_all():
		print field
	
	return http_response.body

def write_page(page):
	with open('download_fetch.html','w') as f:
		f.write(page)

if __name__ == '__main__':
	page = fetch("http://api.nuomi.com/api/dailydeal?version=v1&city=shanghai")
	write_page(page)
