__author__ = 'Decker'


class Filter(object):
    def __init__(self, register_line):
        self._register_line = register_line
        return

    def should_filter(self, content):
        pass


class UrlFilter(Filter):
    def __init__(self, register_line):
        super().__init__(register_line)

    def should_filter(self, url):
        return False


class ElementFilter(Filter):
    def __init__(self, register_line):
        super().__init__(register_line)

    def should_filter(self, html_element):
        return False