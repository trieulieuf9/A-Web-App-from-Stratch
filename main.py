import socket
from server import Server, Request, Response  # import from ./server.py, in the same directory


def main():
    server = Server(port=1111)
    for connection, raw_http_request in server.listen():
        print(raw_http_request)

        request = Request(raw_http_request)

        # request routing
        if request.action == "GET" and (request.path == "/" or request.path == "/home" or request.path == "/index"):
            response = GET_home(request)
        else:
            response = Response(404, body="<h1>Not Found</h1>", headers={"Content-Type": "text/html"})

        connection.sendall(response.to_buffer())


def GET_home(request):
    return Response(200, body="<h1>Home page</h1>", headers={"Content-Type": "text/html"})


main()
