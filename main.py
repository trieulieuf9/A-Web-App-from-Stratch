import socket

## TODO:
## 1. write a Request class, that parse a raw HTTP request string into action, path, headers, body, params
## 2. write a Server class, that can take many requests without quitting run infinitely, only stop when receive a kill signal.

class Response:  # A red room is also a kind of room.
    def __init__(self):
        self.headers = {"Content-Type": "text/plain"}
        self.body = ""
        self.status_code = 200
        self.resp_http_codes = {200: "OK",  # see here for more https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
                                201: "Created",
                                401: "Unauthenticated",
                                403: "Unauthorized",
                                404: "Not Found"}

    def _build_http_code(self):
        return "HTTP/1.1 {} {}".format(self.status_code, self.resp_http_codes[self.status_code])

    def _build_headers(self):
        resp_headers = ""
        for key, value in self.headers.items():
            resp_headers += "{}: {}\n".format(key, value)

        resp_headers += "Content-Length: {}".format(len(self.body))
        return resp_headers

    def to_string(self):
        response = self._build_http_code() + "\n" + self._build_headers()
        response += "\n\n"  # padding between header and body
        response += self.body
        return response

    def to_buffer(self):
        return self.to_string().encode("utf-8")


response = Response()
response.body = "hello"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(('127.0.0.1', 1111))
    s.listen()

    for i in range(2):
        print("connection", i)
        connection, addr = s.accept()

        with connection:
            print('Connected by', addr)

            data = connection.recv(1024)
            request = data.decode("utf-8")
            print("--- Request ---")
            print(request)
            print("--- Response ---")
            print(response.to_string())

            # conn.send(response_header)
            # conn.send(content_length)
            # conn.send(padding)
            connection.sendall(response.to_buffer())
