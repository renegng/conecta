#!/usr/bin/python
import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/conecta.rxdbit.com/conecta/")

from swing_main import app as application
