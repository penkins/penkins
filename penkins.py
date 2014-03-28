#!/usr/bin/env python

import git
import yaml
import BaseHTTPServer
import os
import sys
import subprocess

PORT = 8001


class PenkinsWebServer(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """
        respond to a GET-request
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        project_name = self.path[1:]
        # self.wfile.write(self.path[1:])

        if os.path.isfile('ci/%s.yaml' % project_name):
            task = yaml.load(open('ci/%s.yaml' % project_name, 'r'))
            # print task

            if task['work'] == 'build':
                if 'build_count' in task:
                    task['build_count'] += 1
                else:
                    task['build_count'] = 1

                # TODO: execute commands 'before'

                git.Git().clone(task['repository'], "%s/%s/%s" % (task['path'], project_name, task['build_count']))
                # print "clone"

                # TODO: execute commands 'after'
            elif task['work'] == 'update':
                # TODO: execute commands 'before'

                log = git.cmd.Git(task['path']).pull()

                # log_file = open('log/%s.log' % project_name, 'w')
                # log_file.write(log)
                # log_file.write('\n---\n')
                # log_file.close()

                # TODO: execute commands 'after'

            y_doc = open('ci/%s.yaml' % project_name, 'w')
            y_doc.write(yaml.dump(task))
            y_doc.close()

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(("", PORT), PenkinsWebServer)

    httpd.serve_forever()
    httpd.server_close()