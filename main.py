from wsgiref.simple_server import make_server
from app import app

if __name__ == '__main__':
    with make_server('', 8080, app) as httpd:
        print('server starting on 0.0.0.0:8080...')
        httpd.serve_forever()