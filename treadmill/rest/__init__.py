"""
Treadmill REST base module
"""


import abc
import logging
import importlib
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import tornado.netutil

import flask


FLASK_APP = flask.Flask(__name__)
FLASK_APP.config['BUNDLE_ERRORS'] = True

_LOGGER = logging.getLogger(__name__)


class RestServer(object):
    """REST Server."""

    @abc.abstractmethod
    def _setup_auth(self):
        """Setup the http authentication."""
        pass

    @abc.abstractmethod
    def _setup_endpoint(self, http_server):
        """Setup the http server endpoint."""
        pass

    def run(self):
        """Start server."""
        self._setup_auth()

        FLASK_APP.config['REST_SERVER'] = self

        container = tornado.wsgi.WSGIContainer(FLASK_APP)
        http_server = tornado.httpserver.HTTPServer(container)

        self._setup_endpoint(http_server)

        tornado.ioloop.IOLoop.current().start()


class TcpRestServer(RestServer):
    """TCP based REST Server."""

    def __init__(self, port, host='0.0.0.0', auth_type=None, protect=None,
                 workers=0):
        """Init methods

        :param int port: port number to listen on (required)
        :param str host: host IP to listen on, default is '0.0.0.0'
        :param str auth_type: the auth type, default is None
        :param str protect: which URLs to protect, default is None
        :param int workers: the number of workers to be forked, defaults to 0,
            which is 5 in tornado, I know, weird, but that is their defaults.
        """
        self.port = int(port)
        self.host = host
        self.auth_type = auth_type
        self.protect = protect
        self.workers = workers

    def _setup_auth(self):
        """Setup the http authentication."""
        if self.auth_type is not None:
            _LOGGER.info('Starting REST server: %s:%s, auth: %s, protect: %r',
                         self.host, self.port, self.auth_type, self.protect)
            try:
                mod = importlib.import_module(
                    'treadmill.plugins.rest.auth.' + self.auth_type)
                FLASK_APP.wsgi_app = mod.wrap(FLASK_APP.wsgi_app, self.protect)
            except:
                _LOGGER.exception('Unable to load auth plugin.')
                raise
        else:
            _LOGGER.info('Starting REST (noauth) server on %s:%i',
                         self.host, self.port)

    def _setup_endpoint(self, http_server):
        """Setup the http server endpoint."""
        if self.workers:
            http_server.bind(self.port)
            http_server.start(self.workers)
        else:
            http_server.listen(self.port)


class UdsRestServer(RestServer):
    """UNIX domain socket based REST Server."""

    def __init__(self, socket):
        """Init method."""
        self.socket = socket

    def _setup_auth(self):
        """Setup the http authentication."""
        _LOGGER.info('Starting REST (noauth) server on %s', self.socket)

    def _setup_endpoint(self, http_server):
        """Setup the http server endpoint."""
        unix_socket = tornado.netutil.bind_unix_socket(self.socket)
        http_server.add_socket(unix_socket)
