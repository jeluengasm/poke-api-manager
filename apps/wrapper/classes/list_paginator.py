from collections import OrderedDict
from typing import List

from django.core.paginator import EmptyPage, Paginator
from rest_framework.request import Request


class ListPaginator:
    """
    A class that paginates a list of objects based on the provided offset and
    limit.
    """

    def __init__(self, request: Request):
        self._url_scheme = request.scheme
        self._host = request.get_host()
        self._path_info = request.path_info

    def paginate_list(self, data: List, limit: int, offset: int) -> dict:
        """
        Paginates a list of data.

        Args:
            data (List): The list of data to be paginated.
            limit (int): The maximum number of items per page.
            offset (int): The number of items to skip before starting the page.

        Returns:
            dict: A dictionary containing the paginated data, along with
            metadata such as the total count, previous and next URLs.

        Raises:
            EmptyPage: If the requested page is empty.
        """
        page_number = offset // limit + 1
        orphans = offset % limit
        paginator = Paginator(data, limit, orphans=orphans)
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
