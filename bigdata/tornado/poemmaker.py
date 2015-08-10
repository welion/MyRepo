#!/usr/bin/env python

import os
import time

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')
	
class BookHandler(tornado.web.RequestHandler):
	def get(self):
		system_time = str(time.ctime())	
		self.render('book.html',
			title="Home Page",
			systime = system_time,
			books=[
				'Learning python',
				'A hard way to python',
				'Head First: python'
			])


class PoemPageHandler(tornado.web.RequestHandler):
	def post(self):
		noun1 = self.get_argument('noun1')
		noun2 = self.get_argument('noun2')
		verb  = self.get_argument('verb')
		noun3 = self.get_argument('noun3')
		self.render('poem.html', roads=noun1, wood=noun2, made=verb, difference=noun3)

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[(r'/',IndexHandler),
			  (r'/poem',PoemPageHandler),
			  (r'/book',BookHandler),
			  
		],
		template_path=os.path.join(os.path.dirname(__file__),"templates")
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
