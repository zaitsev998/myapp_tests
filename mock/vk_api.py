import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint
from threading import Thread
import pymysql
from pymysql.cursors import DictCursor
import settings


class VKApiHandleRequests(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.startswith('/vk_id'):
            username = self.path[7:]
            connection = pymysql.connect(host=settings.DB_HOST, port=settings.DB_PORT, user=settings.DB_USER,
                                         password=settings.DB_PASS, db=settings.DB_NAME,
                                         charset='utf8', cursorclass=DictCursor, autocommit=True)
            cursor = connection.cursor()
            query = f"SELECT * from test_users WHERE username='{username}'"
            cursor.execute(query)
            if cursor.fetchall():
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'vk_id': randint(100000, 10000000)}
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


class VKApiHTTPMock:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stop_server = False
        self.handler = VKApiHandleRequests
        self.handler.data = None
        self.server = HTTPServer((self.host, self.port), self.handler)

    def start(self):
        self.server.allow_reuse_address = True
        th = Thread(target=self.server.serve_forever, daemon=True)
        th.start()
        return self.server

    def stop(self):
        self.server.server_close()
        self.server.shutdown()
