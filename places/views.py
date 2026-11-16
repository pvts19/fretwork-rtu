from django.http import HttpResponse, HttpResponseNotFound
from django.utils.html import escape

from homepage.page import page
from place_service import find_place
from storage import load_places, load_visits
from visit_service import place_rating


def place_list(request):
    cards = "".join(f"""
      <div class="col-md-4 mb-3"><div class="card h-100 shadow-sm">
        <div class="card-body">
          <span class="badge bg-success mb-2">{escape(p.category)}</span>
          <h5 class="card-title">{escape(p.name)}</h5>
          <p class="card-text text-muted">{escape(p.address)}</p>
          <p class="card-text">{p.price} руб./чел. · {p.hours}</p>
          <a href="/places/{p.id}/" class="btn btn-sm btn-success">
            Подробнее</a>
        </div></div></div>""" for p in load_places())
    content = f'<h1 class="mb-4">Места для отдыха</h1>' \
              f'<div class="row">{cards}</div>'
    return HttpResponse(page("Места — RestSpot", content))


def place_detail(request, place_id):
    place = find_place(load_places(), place_id)
    if place is None:
        return HttpResponseNotFound(
            page("Не найдено", "<h1>Место не найдено</h1>"))
    visits = load_visits()
    rating = place_rating(visits, place.id) or "нет оценок"
    rows = "".join(
        f'<li class="list-group-item"><a href="/visits/{v.id}/">'
        f'{v.date}</a> — {v.people} чел.</li>'
        for v in visits if v.place_id == place.id and v.is_active
    ) or '<li class="list-group-item">Нет запланированных посещений</li>'
    content = f"""
    <a href="/places/">&larr; Все места</a>
    <h1 class="mt-2">{escape(place.name)}</h1>
    <p><span class="badge bg-success">{escape(place.category)}</span></p>
    <ul>
      <li>Адрес: {escape(place.address)}</li>
      <li>Цена: {place.price} руб./чел.</li>
      <li>Вместимость: {place.capacity} чел.</li>
      <li>Часы работы: {place.hours}</li>
      <li>Рейтинг: {rating}</li>
    </ul>
    <h4>Запланированные посещения</h4>
    <ul class="list-group">{rows}</ul>"""
    return HttpResponse(page(f"{place.name} — RestSpot", content))
