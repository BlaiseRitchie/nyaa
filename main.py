#	Sample main.py Tornado file
# 
#	Author: Mike Dory
#		11.12.11
#

#!/usr/bin/env python
import os.path
import os
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import unicodedata
import urllib
import re
from xml.dom.minidom import parseString

# import and define tornado-y things
from tornado.options import define, options
define("port", default=5000, help="run on the given port", type=int)

# the main page
class MainHandler(tornado.web.RequestHandler):
	def get(self):
		get(self, None)

	def get(self, q):

		link = "http://www.nyaa.eu/?page=rss"

		if q != None:
			link += "&term=" + q

		linkopen = urllib.urlopen(link)


		if linkopen != None:
			if str(linkopen.headers).find('charset') != -1:
				charset = re.search("^Content-Type: text/xml; charset=(?P<charset>.*?)\r\n",str(linkopen.headers))
				if charset != None:
					charset = charset.group('charset')
			if charset == None:
				charset = 'utf-8'

			xml = parseString(linkopen.read().decode(charset).encode('utf-8')).getElementsByTagName('channel')[0]

			page_heading = title = xml.getElementsByTagName('title')[0].firstChild.nodeValue

			content = '<h3>Results:</h3>'

			results = []

			for item in xml.getElementsByTagName('item'):
				ititle = item.getElementsByTagName('title')[0].firstChild.nodeValue
				if ititle == None:
					break

				id = re.search("http://www\.nyaa\.eu/\?page=download&tid=(?P<id>\d*)", item.getElementsByTagName('link')[0].firstChild.nodeValue)
				if id != None:
					id = id.group('id')
				else:
					break

				description = item.getElementsByTagName('description')[0].firstChild.nodeValue

				result = {"title": ititle,
				          "id": id,
				          "description": description }
				results.append(result)

		else:
			page_heading = title = "Error"
			

		self.render(
			"index.html",
			title = title,
			page_heading = page_heading,
			results = results
		)

# application settings and handle mapping info
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/search/(.*)", MainHandler)
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)

# RAMMING SPEEEEEEED!
def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(os.environ.get("PORT", 5000))

	# start it up
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()
