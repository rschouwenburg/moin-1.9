# -*- coding: iso-8859-1 -*-
"""
    MoinMoin - FastCGI Request Implementation for fastcgi and Apache
    (and maybe others).

    @copyright: 2001-2003 by J�rgen Hermann <jh@web.de>,
                2003-2006 MoinMoin:ThomasWaldmann
    @license: GNU GPL, see COPYING for details.
"""
import sys, os
from MoinMoin import config
from MoinMoin.request import RequestBase

class Request(RequestBase):
    """ specialized on FastCGI requests """

    def __init__(self, fcgRequest, env, form, properties={}):
        """ Initializes variables from FastCGI environment and saves
            FastCGI request and form for further use.

            @param fcgRequest: the FastCGI request instance.
            @param env: environment passed by FastCGI.
            @param form: FieldStorage passed by FastCGI.
        """
        try:
            self.fcgreq = fcgRequest
            self.fcgenv = env
            self.fcgform = form
            self._setup_vars_from_std_env(env)
            RequestBase.__init__(self, properties)

        except Exception, err:
            self.fail(err)

    def _setup_args_from_cgi_form(self):
        """ Override to use FastCGI form """
        return RequestBase._setup_args_from_cgi_form(self, self.fcgform)

    def read(self, n=None):
        """ Read from input stream. """
        if n is None:
            return self.fcgreq.stdin.read()
        else:
            return self.fcgreq.stdin.read(n)

    def write(self, *data):
        """ Write to output stream. """
        self.fcgreq.out.write(self.encode(data))

    def flush(self):
        """ Flush output stream. """
        self.fcgreq.flush_out()

    def finish(self):
        """ Call finish method of FastCGI request to finish handling of this request. """
        RequestBase.finish(self)
        self.fcgreq.finish()

    def _emit_http_headers(self, headers):
        """ private method to send out preprocessed list of HTTP headers """
        for header in headers:
            self.write("%s\r\n" % header)
        self.write("\r\n")

