__author__ = 'Decker'

import urllib

class ad_list_loader(object):
    def __init__(self, ad_list_content):
        self.ad_list_content = str(ad_list_content)
        self.blocked_urls = []
        self.hide_elements = []

    def resolve_blocked_urls(self):
        for line in self.ad_list_content.splitlines():
            if line.startswith('#'):
                continue
