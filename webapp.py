from werkzeug.wrappers import Request, Response
from datetime import date
import datetime
import parser

class WebApp(object):
    def wsgi_app(self, environ, start_response):
        request = Request(environ, start_response)
        valid = True
        channel = request.args.get('channel', None)
        if not channel:
            valid = False
            text = '{"error":"Channel name is required"}'
        if valid:
            d = request.args.get('date', date.today())
            if type(d) == type('str'):
                d = datetime.date(*[int(a) for a in d.split('-')])
                if not d:
                    d = date.today()

            meta = request.args.get('meta', False)

            details = request.args.get('details', False)

            indent = request.args.get('indent', None)
            if indent:
                indent = int(indent)
            else:
                indent = 4

            text = str(parser.get_show_list(channel, d, meta, details, indent))
            if not text:
                text = '"error":"Channel name {0} seems invalid."'.format(request.args.get('channel'))
        response = Response(text, content_type='application/json; charset=utf-8')
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)
