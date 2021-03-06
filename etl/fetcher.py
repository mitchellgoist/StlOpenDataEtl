#!/usr/bin/env python3

import os
import ssl
import sys
import yaml
from app import ROOT_DIR
from etl.fetcher_response import FetcherResponse
from etl.payload_data import PayloadData
from etl.utils import get_file_name_from_uri
from io import BytesIO
from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import URLError


class Fetcher:

    def fetch_all(self, src_yaml):
        '''
        Returns a list of fetcher data objects as defined below.
        '''
        data = []
        for key in src_yaml.keys():
            data.append(self.fetch(key, src_yaml[key]['url']))

        return data

    def fetch(self, name, url):
        '''
        Returns a fetcher data object.

        Arguments:
        name -- a friendly name for a given source
        url -- the url from which the fetcher will attempt to fetch

        '''
        try:
            # start hack - ignoring SSL completely - see https://stackoverflow.com/questions/27835619/urllib-and-ssl-certificate-verify-failed-error
            ssl_context = ssl._create_unverified_context()
            response = urlopen(url, context=ssl_context)
            # end hack
            return FetcherResponse(name, [PayloadData(get_file_name_from_uri(url), BytesIO(response.read()))], url, None)

        except URLError as url_error:
            return FetcherResponse(name, None, url, url_error)

        error_message = 'An error has occurred.'
        return FetcherResponse(name, None, url, error_message)
