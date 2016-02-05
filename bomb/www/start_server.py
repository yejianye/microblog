#!/usr/bin/env python
"""Start microblog API server"""
import argparse
from webrpc.server import Server
from bomb.www.app import api_site

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--port", type=int, default=7431,  help="Server port")
    args = parser.parse_args()
    api_site.run(host='0.0.0.0', port=args.port)
