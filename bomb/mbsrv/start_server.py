#!/usr/bin/env python
"""Start microblog internal service"""
import argparse
from bomb.mbsrv.app import mbsrv_site

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--port", type=int, default=7777,  help="Server port")
    args = parser.parse_args()
    mbsrv_site.run(host='0.0.0.0', port=args.port)

