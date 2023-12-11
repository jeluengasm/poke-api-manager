from collections import OrderedDict
from typing import List

from django.core.paginator import EmptyPage, Paginator
from rest_framework.request import Request


class ListPaginator:
    def __init__(self, request: Request):
        self._url_scheme = request.scheme
        self._host = request.get_host()
        self._path_info = request.path_info

    def paginate_list(self, data: List, limit: int, offset: int) -> dict:
        page_number = offset // limit + 1
        paginator = Paginator(data, limit)
        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
            page.object_list = []

        previous_url = None
        next_url = None
        if self._host and self._path_info:
            if page.has_previous():
                previous_url = "{}://{}{}?offset={}&limit={}".format(
                    self._url_scheme,
                    self._host,
                    self._path_info,
                    offset - limit,
                    limit,
                )
            if page.has_next():
                next_url = "{}://{}{}?offset={}&limit={}".format(
                    self._url_scheme,
                    self._host,
                    self._path_info,
                    offset + limit,
                    limit,
                )

        response_dict = OrderedDict([
            ("count", len(data)),
            ("next", next_url),
            ("previous", previous_url),
            ("results", page.object_list),
        ])
        return response_dict
