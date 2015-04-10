__author__ = 'Decker'


class HttpRequest(object):
    def __init__(self, input_bytes):
        self.input_bytes = b''
        self.request_line = b''
        self.headers = {}
        self.body = b''
        self.load_from_binary(input_bytes)

    def load_from_binary(self, input_bytes):
        self.input_bytes = input_bytes
        firstly = self.input_bytes.split(b'\r\n\r\n')
        if len(firstly) != 2:
            raise RuntimeError('This stream is not a HTTP stream')
        self.body = firstly[1]
        secondly = firstly[0].split(b'\r\n')
        self.request_line = secondly[0]
        for i in range(1, len(secondly)):
            if not secondly[i]:
                continue
            k = secondly[i][:secondly[i].index(b':')]
            v = secondly[i][secondly[i].index(b':') + 1:]
            self.headers[k] = v

    def to_binary(self):
        stream = self.request_line
        stream = stream.__add__(b'\r\n')
        for key in self.headers.keys():
            stream = stream.__add__(key)
            stream = stream.__add__(b':')
            stream = stream.__add__(self.headers[key])
            stream = stream.__add__(b'\r\n')
        stream = stream.__add__(b'\r\n')
        stream = stream.__add__(self.body)
        return stream