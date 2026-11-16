from django.http import HttpResponse

from homepage.page import page
from storage import load_places, load_visits


def index(request):
    places = load_places()
    active = [v for v in load_visits() if v.is_active]
    content = f"""
    <div class="p-5 mb-4 bg-white rounded-3 shadow-sm">
      <h1 class="display-5">RestSpot</h1>
      <p class="lead">Сервис поиска мест для отдыха: парки, кафе, пляжи,
         музеи и базы отдыха. Подберите место по бюджету и запланируйте
         поход с друзьями.</p>
      <p>Мест в каталоге: <b>{len(places)}</b>,
         активных посещений: <b>{len(active)}</b>.</p>
      <a class="btn btn-success" href="/places/">Смотреть места</a>
      <a class="btn btn-outline-success" href="/visits/">Посещения</a>
    </div>"""
    return HttpResponse(page("RestSpot", content))
