# 🤖 CyberStore — Киберпанк-магазин

> Домашнее задание с курса «Python-разработчик»

Простое веб-приложение на чистом Python с вёрсткой в стиле киберпанк.

---

## 🚀 Быстрый старт

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/Kurai1369/kurai_cyberpunk_shop.git
cd kurai_cyberpunk_shop

# 2. (Опционально) Создайте виртуальное окружение
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Запустите сервер
python server.py

# 4. Откройте в браузере
http://localhost:8000
```

## 📁 Структура проекта
```
├── .gitignore          # Исключения для Git
├── README.md           # Файл, который вы сейчас читаете
├── server.py           # Веб-сервер на http.server
├── style.css           # Все стили киберпанк-темы
├── bg.jpg              # Фоновое изображение
├── main.html           # Страница «Главная»
├── categories.html     # Страница «Категории»
├── orders.html         # Страница «Заказы»
└── contacts.html       # Страница «Контакты» (форма + POST)
```

## ✨ Особенности

🎨 Киберпанк-дизайн: неоновые цвета, шрифты Orbitron/Rajdhani, глитч-эффекты  
📱 Адаптивная вёрстка на Bootstrap 5  
🔧 Чистый Python: без фреймворков, только стандартная библиотека (http.server)  
📡 Обработка запросов:  
GET /* → рендеринг HTML-страниц  
POST /contacts → приём и логирование данных формы  
🖼️ Статика: сервер отдаёт CSS и изображения с правильными заголовками  

## 📬 Контакты

Автор: @Kurai1369
Почта: kurai@vk.com
Дата: Апрель 2026