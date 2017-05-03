import os
import json
import socket
import time
import subprocess as sp

from tornado import web

from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler

# from jupyterhub.utils
def random_port():
    """get a single random port"""
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

# Data shared between handler requests
state_data = dict()

class RefineProxyHandler(IPythonHandler):
    '''Manage an OpenRefine session instance.'''

    # refine command.
    cmd = [
        'refine',
    ]
    env = {
        'JAVA_OPTIONS' : "-Drefine.headless=true -Djava.security.egd=file:/dev/urandom"
    }

    def initialize(self, state):
        self.state = state

    def refine_uri(self):
        return '{}proxy/{}/'.format(self.base_url, self.state['port'])

    def gen_response(self, proc):
        response = {
            'pid': proc.pid,
            'url':self.refine_uri(),
        }
        return response
        
    def is_running(self):
        '''Check if our proxied process is still running.'''

        if 'proc' not in self.state:
            return False
        elif 'port' not in self.state:
            return False

        # Check if the process is still around
        proc = self.state['proc']
        if proc.poll() == 0:
            del(self.state['proc'])
            self.log.debug('Cannot poll on process.')
            return False
        
        # Check if it is still bound to the port
        port = self.state['port']
        sock = socket.socket()
        try:
            self.log.debug('Binding on port {}.'.format(port))
            sock.bind(('', port))
        except OSError as e:
            self.log.debug('Bind error: {}'.format(str(e)))
            if e.strerror != 'Address already in use':
                return False

        sock.close()

        return True

    def is_available(self):
        pass
        
    @web.authenticated
    def post(self):
        '''Start a new refine session.'''

        if self.is_running():
            proc = self.state['proc']
            port = self.state['port']
            self.log.info('Resuming process on port {}'.format(port))
            response = self.gen_response(proc)
            self.finish(json.dumps(response))
            return

        self.log.debug('No existing process')

        port = random_port()

        cmd = self.cmd + [
            '-p', str(port)
        ]

        server_env = os.environ.copy()
        server_env.update(self.env)

        # Runs refine in background
        proc = sp.Popen(cmd, env=server_env)

        if proc.poll() == 0:
            raise web.HTTPError(reason='refine session terminated', status_code=500)
            self.finish()

        # Wait for refine to be available
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        refine_attempts = 0
        while refine_attempts < 5:
            try:
                sock.connect(('', port))
                break
            except socket.error as e:
                print('sleeping: {}'.format(e))
                time.sleep(2)
                refine_attempts += 1

        # Store our process
        self.state['proc'] = proc
        self.state['port'] = port

        response = self.gen_response(proc)
        self.finish(json.dumps(response))

    @web.authenticated
    def get(self):
        if self.is_running():
            proc = self.state['proc']
            port = self.state['port']
            self.log.info('Process exists on port {}'.format(port))
            response = self.gen_response(proc)
            self.finish(json.dumps(response))
            return
        self.finish(json.dumps({}))
 
    @web.authenticated
    def delete(self):
        if 'proc' not in self.state:
            raise web.HTTPError(reason='no refine running', status_code=500)
        proc = self.state['proc']
        proc.kill()
        self.finish()

def setup_handlers(web_app):
    host_pattern = '.*$'
    route_pattern = ujoin(web_app.settings['base_url'], '/refineproxy/?')
    web_app.add_handlers(host_pattern, [
        (route_pattern, RefineProxyHandler, dict(state=state_data))
    ])

# vim: set et ts=4 sw=4:
