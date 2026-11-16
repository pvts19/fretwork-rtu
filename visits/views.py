from django.http import HttpResponse, HttpResponseNotFound
from django.utils.html import escape

from homepage.page import page
from models.visit import STATUSES
from place_service import find_place
from storage import load_places, load_users, load_visits


def visit_list(request):
    places = load_places()
    users = {u.id: u for u in load_users()}
    rows = []
    for v in sorted(load_visits(), key=lambda v: v.date):
        place = find_place(places, v.place_id)
        user = users.get(v.user_id)
        rows.append(f"""<tr>
          <td><a href="/visits/{v.id}/">№{v.id}</a></td><td>{v.date}</td>
          <td><a href="/places/{v.place_id}/">
            {escape(place.name if place else '?')}</a></td>
          <td>{escape(user.name if user else '?')}</td>
          <td>{v.people}</td><td>{STATUSES[v.status]}</td></tr>""")
    content = f"""<h1 class="mb-4">Посещения</h1>
    <table class="table table-striped bg-white">
      <thead><tr><th>№</th><th>Дата</th><th>Место</th><th>Пользователь</th>
        <th>Человек</th><th>Статус</th></tr></thead>
      <tbody>{''.join(rows)}</tbody></table>"""
    return HttpResponse(page("Посещения — RestSpot", content))


def visit_detail(request, visit_id):
    visit = next((v for v in load_visits() if v.id == visit_id), None)
    if visit is None:
        return HttpResponseNotFound(
            page("Не найдено", "<h1>Посещение не найдено</h1>"))
    place = find_place(load_places(), visit.place_id)
    user = next((u for u in load_users() if u.id == visit.user_id), None)
    content = f"""
    <a href="/visits/">&larr; Все посещения</a>
    <h1 class="mt-2">Посещение №{visit.id}</h1>
    <ul>
      <li>Место: <a href="/places/{visit.place_id}/">
        {escape(place.name if place else '?')}</a></li>
      <li>Пользователь: {escape(user.name if user else '?')}</li>
      <li>Дата: {visit.date}</li>
      <li>Человек: {visit.people}</li>
      <li>Стоимость: {place.cost(visit.people) if place else '?'} руб.</li>
      <li>Статус: {STATUSES[visit.status]}</li>
      <li>Оценка: {visit.rating or '—'}</li>
    </ul>"""
    return HttpResponse(page(f"Посещение №{visit.id}", content))
