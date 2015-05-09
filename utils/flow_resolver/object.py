__author__ = 'Decker'


class HttpObject(object):
    def __init__(self, input_bytes):
        self.request_line = b''
        self.headers = {}
        self.body = b''
        self.finished = False
        if input_bytes:
            self.load_from_binary(input_bytes)

    def load_from_binary(self, input_bytes):
        if b'\r\n\r\n' not in input_bytes:
            raise RuntimeError('This stream is not a HTTP stream')
        header_range = input_bytes[:input_bytes.index(b'\r\n\r\n')] or b''
        header_split = header_range.splitlines()
        self.request_line = header_split[0]
        for i in range(1, len(header_split)):
            if not header_split[i]:
                continue
            k = header_split[i][:header_split[i].index(b':')]
            v = header_split[i][header_split[i].index(b':') + len(b':'):]
            self.headers[k] = v
        if b'Transfer-Encoding' in self.headers and b'chunked' in self.headers[b'Transfer-Encoding']:
            self.resolve_chunked_data(input_bytes[input_bytes.index(b'\r\n\r\n') + len(b'\r\n\r\n'):])
        elif b'Content-Length' in self.headers:
            self.resolve_common_data(input_bytes[input_bytes.index(b'\r\n\r\n') + len(b'\r\n\r\n'):] or b'')
        else:
            self.finished = True

    def to_binary(self):
        # remove encoding

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

    def to_common_binary(self):
        self.headers[b'Transfer-Encoding'] = b''
        self.headers[b'Content-Length'] = str(len(self.body)).encode()
        self.headers[b'catched-flow'] = b'yes'
        return self.to_binary()

    def get_is_finished(self):
        return self.finished

    def resolve_chunked_data(self, data):
        self.body = self.body.__add__(data)
        if data.endswith(b'0\r\n\r\n'):
            self.finished = True
            self.body = self.decode_chunked_body()
        else:
            return

    def resolve_common_data(self, data):
        self.body = self.body.__add__(data)
        if len(self.body) == int(self.headers[b'Content-Length'].decode()):
            self.finished = True

    def append_body(self, data):
        if self.finished:
            raise RuntimeError('If data is finished transfer, its not allowed to change')

        if b'Transfer-Encoding' in self.headers and self.headers[b'Transfer-Encoding'] != b'chunked':
            self.resolve_chunked_data(data)
        else:
            self.resolve_common_data(data)

    def decode_chunked_body(self):
        encoded = self.body
        new_data = b''
        while len(encoded):
            off = int(encoded[:encoded.index(b'\r\n')], 16)
            if off == 0:
                break
            encoded = encoded[encoded.index(b'\r\n') + 2:]
            new_data = new_data.__add__(encoded[:off])
            encoded = encoded[off + 2:]

        return new_data
