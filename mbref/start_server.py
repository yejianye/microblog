#!/usr/bin/env python
"""Start microblog API server"""
import argparse
import mbref.app

def gevent_server(app, port):
    import gevent.monkey
    from gevent.wsgi import WSGIServer
    gevent.monkey.patch_all()
    http_server = WSGIServer(('', port), app)
    http_server.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--gevent", default=False, action='store_true',
                        help="Use gevent for concurrency")
    parser.add_argument("--port", type=int, default=7431,  help="Server port")
    args = parser.parse_args()

    if args.gevent:
        app = mbref.app.create_app()
        gevent_server(app, args.port)
    else:
        app = mbref.app.create_app()
        app.run(host='0.0.0.0', port=args.port)
