from django.core.paginator import Paginator


def paginate(request, queryset, per_page=6):
    """Возвращает страницу результатов и строку GET-параметров без page,
    чтобы фильтры и сортировка сохранялись при переходе между страницами."""
    page_obj = Paginator(queryset, per_page).get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)
    return page_obj, params.urlencode()
