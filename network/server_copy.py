#-*- coding: utf-8 -*-
#!/usr/bin/env python

import tornado
import tornado.web
import tornado.httpserver
from tornado.options import define,options

define("port", default=4444, type=int)



class ExampleHandler(tornado.web.RequestHandler):

	def get(self):
		print "------GET------"
		who = self.get_argument("who",None)
		if who:
			self.write("Hello, " + who)
		else :
			self.write("Hello world .... ")

	def post(self):
		print "-------POST------"
		who = self.get_argument("who",None)
                if who:
                        self.write("Hello, " + who)
                else :
                        self.write("Hello world")

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/",ExampleHandler), 
		#	(r"/deal",DealHandler),
		]
		settings = dict()
		tornado.web.Application.__init__(self, handlers, settings)


def create_server():
	tornado.options.parse_command_line() #define porti
#	app = tornado.web.Application(handlers=[(r"/", ExampleHandler)])
	app = Application()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	create_server()
