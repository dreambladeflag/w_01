import os
from wsgiref import util


class Response:
    def __init__(self, content, status = None, headers = None):
        self.__CONTENT = content
        self.__STATUS = status or 200
        self.__HEADERS = headers or [('Content-type', 'text/plain; charset=utf-8')]

    def get_http_status(self):
        desc = 'OK'

        if self.__STATUS != 200:
            desc = 'FAIL'

        return '{} {}'.format(self.__STATUS, desc)

    def get_http_headers(self):
        return self.__HEADERS

    def get_http_content(self):
        if isinstance(self.__CONTENT, util.FileWrapper):
            return self.__CONTENT
        return [str(self.__CONTENT).encode('utf-8')]


class SimpleFramework:
    def __init__(self):
        self.__ROUTES = {}

    def __call__(self, environ, start_response):
        fn = environ['PATH_INFO'][1:]
        if os.path.exists(fn):
            start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
            return util.FileWrapper(open(fn, 'rb'))

        k = '{}|{}'.format(environ['PATH_INFO'], environ['REQUEST_METHOD'])

        if k not in self.__ROUTES:
            start_response('404 NOT FOUND', [('Content-type', 'text/html; charset=utf-8')])
            return [b'404 NOT FOUND']

        resp = self.__ROUTES[k]()

        if not isinstance(resp, Response):
            start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
            return [str(resp).encode('utf-8')]

        start_response(resp.get_http_status(), resp.get_http_headers())
        return resp.get_http_content()

    def route(self, path, methods):
        def route_decoration(func):
            for method in methods:
                self.__ROUTES['{}|{}'.format(path, str(method).upper())] = func

        return route_decoration


def response(content, status = None, headers = None):
    return Response(content, status, headers)

def response_json(content, status = None):
    return response(content, status, [('Content-type', 'application/json; charset=utf-8')])

def render_html(filename):
    if not os.path.exists(filename):
        raise RuntimeError('File {} not exists'.format(filename))
    return Response(util.FileWrapper(open(filename, 'rb')), headers=[('Content-type', 'text/html; charset=utf-8')])
