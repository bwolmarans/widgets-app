#!/usr/bin/env python3
"""
Usage: ./server.py [<port>]
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import requests
from random import randint

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()

        i = randint(1, 5)
        r =requests.get('http://widgets-widget:3000/widget/' + str(i))
        wgt = r.text
        #print(t)

        i = randint(1, 5)
        r =requests.get('http://widgets-quantity:3001/quantity/' + str(i))
        qty = r.text
        #print(t)

        i = randint(1, 5)
        r =requests.get('http://widgets-warehouse:3002/warehouse/' + str(i))
        whs = r.text
        #print(t)
        #self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
        x = "Thank you for checking the Widgets inventory. Happy Selling! \n" + str(wgt) + "\n" + str(qty) + "\n " + str(whs) + "\n"
        self.wfile.write(x.encode('utf-8'))
        #self.wfile.write("Thank you for checking the Widgets inventory. Happy Selling! " + wgt + " " + qty + " " + whs + " ".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=80):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
