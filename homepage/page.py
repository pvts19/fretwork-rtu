"""Сборка HTML-страницы с общим оформлением (до перехода на шаблоны)."""
from django.utils.html import escape

BOOTSTRAP = ('https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/'
             'bootstrap.min.css')


def page(title: str, content: str) -> str:
    """Оборачивает content в HTML-документ с навигацией и Bootstrap."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="{BOOTSTRAP}">
  <style>body {{ background: #f4f8f6; }}</style>
</head>
<body>
  <nav class="navbar navbar-expand navbar-dark bg-success mb-4">
    <div class="container">
      <a class="navbar-brand" href="/">RestSpot</a>
      <div class="navbar-nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/places/">Места</a>
        <a class="nav-link" href="/visits/">Посещения</a>
      </div>
    </div>
  </nav>
  <main class="container">{content}</main>
</body>
</html>"""
