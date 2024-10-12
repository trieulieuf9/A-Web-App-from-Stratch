import socket


class Server:
    def __init__(self, host="127.0.0.1", port=1111):
        self.host = host
        self.port = port

    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))  # s.close()
            s.listen()

            while True:
                connection, addr = s.accept()
                with connection:
                    data = connection.recv(1024)  # TODO: support request bigger than 1024 bytes
                    raw_http_request = data.decode("utf-8")
                    yield connection, raw_http_request


class Response:
    def __init__(self, status_code, body="", headers=dict()):
        self.headers = headers  # {"Content-Type": "text/plain"}
        self.body = body
        self.status_code = status_code
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





class Request:

    def __init__(self, raw_http_request):
        self.raw_http_request = raw_http_request
        lines = raw_http_request.split("\n")
        parts = lines[0].split(" ")  # EX: "GET /example?hello HTTP/1.1"
        self.action = parts[0]
        self.full_path = parts[1]  # path and params
        self.path = parts[1].split("?")[0]
        self.http_protocol = parts[2]
        self.params = self.parse_params(self.full_path)  # dict of keys and values


    def get_path(self):
        return ""

    def parse_params(self, full_path):
        # todo later
        return dict()


def main():
    server = Server()
    for connection, raw_http_request in server.listen():
        print(raw_http_request)

        request = Request(raw_http_request)

        # request routing
        if request.action == "GET" and (request.path == "/" or request.path == "/home" or request.path == "/index"):
            response = home_action(request)
        else:
            response = Response(404, body="<h1>Not Found</h1>", headers={"Content-Type": "text/html"})

        connection.sendall(response.to_buffer())


def home_action(request):
    return Response(200, body="<h1>Home page</h1>", headers={"Content-Type": "text/html"})


main()
