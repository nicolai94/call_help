from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePagination(PageNumberPagination):  # настриваем пагинацию и описываем ее
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),  # ссылка на след страницу
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,  # количество обьектов на странице
            'pages': self.page.paginator.num_pages, # количество страниц
            'results': data  # данные
        })