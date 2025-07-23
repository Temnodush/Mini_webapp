from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# Параметры запуска сервера
hostName = "localhost"
serverPort = 8000




class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Обработка корневого запроса
        if self.path == "/":
            self.path = "/contacts.html"

        try:
            # Проверяем существование файла
            file_path = self.path[1:]
            if not os.path.exists(file_path):
                raise FileNotFoundError

            # Определяем MIME-тип
            if self.path.endswith(".html"):
                mimetype = 'text/html'
            elif self.path.endswith(".css"):
                mimetype = 'text/css'
            elif self.path.endswith(".js"):
                mimetype = 'application/javascript'
            elif self.path.endswith(".jpg") or self.path.endswith(".jpeg"):
                mimetype = 'image/jpeg'
            elif self.path.endswith(".png"):
                mimetype = 'image/png'
            else:
                mimetype = 'text/plain'

            # Читаем и отправляем файл
            with open(file_path, 'rb') as file:  # Бинарный режим!
                content = file.read()

            self.send_response(200)
            self.send_header("Content-type", mimetype)
            self.end_headers()
            self.wfile.write(content)  # Отправляем бинарные данные
        except FileNotFoundError:
            # Если файл не найден, отправляем код 404
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>404 - Page Not Found</h1>")


if __name__ == "__main__":
    # Инициализация и запуск веб-сервера
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started at http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    # Остановка сервера
    webServer.server_close()
    print("Server stopped.")