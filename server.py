from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os
import mimetypes


class CyberHandler(BaseHTTPRequestHandler):

    # Отключаю стандартное логирование (использую своё)
    def log_message(self, format, *args):
        print(f"🌐 {self.address_string()} - {args[0]}")

    def send_file_response(self, file_path, content_type):
        """Вспомогательный метод для отправки файлов с правильными заголовками"""
        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", len(content))
            self.send_header("Cache-Control", "no-cache")  # Отключаем кэш для разработки
            self.end_headers()
            self.wfile.write(content)
            return True
        except FileNotFoundError:
            return False

    def do_GET(self):
        try:
            # Убрала параметры запроса
            path = self.path.split('?')[0]

            # Маршруты для HTML-страниц
            routes = {
                '/': 'main.html',
                '/main.html': 'main.html',
                '/categories.html': 'categories.html',
                '/orders.html': 'orders.html',
                '/contacts.html': 'contacts.html',
            }

            # Обработка статических файлов (CSS, картинки)
            if path.endswith('.css'):
                if self.send_file_response(path[1:], 'text/css; charset=utf-8'):
                    return
            elif path.endswith(('.jpg', '.jpeg')):
                if self.send_file_response(path[1:], 'image/jpeg'):
                    return
            elif path.endswith('.png'):
                if self.send_file_response(path[1:], 'image/png'):
                    return
            elif path.endswith('.gif'):
                if self.send_file_response(path[1:], 'image/gif'):
                    return
            elif path.endswith('.ico'):
                if self.send_file_response(path[1:], 'image/x-icon'):
                    return

            # Обработка HTML-страниц
            html_file = routes.get(path, 'contacts.html')

            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()

            content_bytes = content.encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(content_bytes))
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(content_bytes)

        except ConnectionAbortedError:
            # Если браузер закрыл соединение — логируем
            print(f"⚠️  Соединение закрыто браузером: {self.path}")
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1 style='color:#b026ff; font-family:sans-serif;'>404: File not found</h1>")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            self.send_response(500)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"<h1 style='color:#ff0055; font-family:sans-serif;'>500: {str(e)}</h1>".encode("utf-8"))

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_data_raw = self.rfile.read(content_length).decode("utf-8")

            print("\n" + "=" * 40)
            print("📥 ПОЛУЧЕН POST-ЗАПРОС")
            print(f"🔹 Raw данные: {post_data_raw}")
            print(f"🔹 Raw (decoded): {urllib.parse.unquote(post_data_raw)}")

            if "application/x-www-form-urlencoded" in self.headers.get("Content-Type", ""):
                parsed = urllib.parse.parse_qs(post_data_raw)
                print(f"🔹 Распарсенные данные: {parsed}")
            print("=" * 40 + "\n")

            # Возвращаем полную страницу с подтверждением
            response_html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CyberStore | Сообщение отправлено</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="container-fluid">
    <div class="row">
        <nav class="col-md-3 col-lg-2 d-md-block sidebar">
            <div class="sidebar-header">
                <i class="bi bi-grid-3x3-gap"></i>
                <span class="cyber-title fs-5">Меню</span>
            </div>
            <ul class="nav flex-column">
                <li class="nav-item"><a class="nav-link" href="/main.html"><i class="bi bi-house-door"></i>Главная</a></li>
                <li class="nav-item"><a class="nav-link" href="/categories.html"><i class="bi bi-tags"></i>Категории</a></li>
                <li class="nav-item"><a class="nav-link" href="/orders.html"><i class="bi bi-cart3"></i>Заказы</a></li>
                <li class="nav-item"><a class="nav-link" href="/contacts.html"><i class="bi bi-envelope"></i>Контакты</a></li>
            </ul>
            <div class="user-section">
                <button class="btn user-btn">
                    <img src="https://placehold.co/40/111/b026ff?text=U" class="rounded-circle" alt="Avatar">
                    Пользователь
                </button>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#">Профиль</a></li>
                    <li><a class="dropdown-item" href="#">Выйти</a></li>
                </ul>
            </div>
        </nav>
        <main class="col-md-9 ms-sm-auto col-lg-10 px-md-4 py-4 text-center">
            <div class="cyber-card" style="max-width: 600px; margin: 50px auto;">
                <h1 class="cyber-title mb-4" style="color: #00ff9d;">✅ Успешно!</h1>
                <p class="fs-5 mb-4">Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.</p>
                <div class="d-grid gap-2">
                    <a href="/contacts.html" class="cyber-btn">Вернуться к форме</a>
                    <a href="/main.html" class="cyber-btn" style="border-color: #b026ff; color: #b026ff;">На главную</a>
                </div>
            </div>
        </main>
    </div>
</div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

            content_bytes = response_html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", len(content_bytes))
            self.end_headers()
            self.wfile.write(content_bytes)

        except ConnectionAbortedError:
            print("⚠️  POST: Соединение закрыто браузером")
        except Exception as e:
            print(f"❌ POST ошибка: {e}")


if __name__ == "__main__":
    PORT = 8000

    # Проверяем, не занят ли порт (при первых запусках, почему-то не прогружались страницы)
    import socket

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", PORT))
        except OSError:
            print(f"❌ Порт {PORT} занят! Попробуйте другой.")
            PORT = 8080
            print(f"🔄 Используем порт {PORT} вместо {8000}")

    server = HTTPServer(("localhost", PORT), CyberHandler)
    print(f"\n🚀 Сервер запущен: http://localhost:{PORT}")
    print("📌 Доступные страницы:")
    print("   • http://localhost:{PORT}/ или /main.html - Главная")
    print("   • http://localhost:{PORT}/categories.html - Категории")
    print("   • http://localhost:{PORT}/orders.html - Заказы")
    print("   • http://localhost:{PORT}/contacts.html - Контакты")
    print("📌 Остановите сервер комбинацией Ctrl+C\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Сервер остановлен пользователем.")
        server.server_close()
