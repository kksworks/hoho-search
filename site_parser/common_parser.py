#!/usr/bin/env python3
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
#import mechanize
#import time, os, hashlib, ast
#import datetime
#import shutil
import sys
import urllib
import ssl

import re
import os

from http.cookiejar import CookieJar
from pprint import pprint

import time, datetime

import requests
import subprocess
import shutil

from pathlib import Path
from pathlib import PurePath

from bs4 import BeautifulSoup

#from tools import file_tools
from time import sleep

from urllib.parse import urljoin

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

def get_content_htmlcode(url) :
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)

    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'pl-PL,pl;q=0.8',
            'Connection': 'keep-alive'}

    cookiejarctx = CookieJar()
    opener= urllib.request.build_opener( urllib.request.HTTPCookieProcessor(cookiejarctx) )
    urllib.request.install_opener(opener)
    req = urllib.request.Request(url, None, hdr )

    try:
        page = urllib.request.urlopen(req, timeout=15)

    except Exception as ex :
        print('[err] get page err [%s]'%(ex))
        return None

    content = page.read()

    return content


def get_content_bs4ctx(url) :
    bs4ctx = None
    try:
        html_code = get_content_htmlcode(url)
        bs4ctx = BeautifulSoup(html_code, "html.parser")
    except:
        return None

    return bs4ctx


def url_join(url1, url2):
    return urljoin(url1, url2)
