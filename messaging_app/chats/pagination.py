from rest_framework.pagination import PageNumberPagination

class CustomMessagePagination(PageNumberPagination):
    page_size = 20  # default messages per page
    page_size_query_param = 'page_size'  # allows ?page_size=50 in query
    max_page_size = 100  # max limit client can request
