from rest_framework.pagination import PageNumberPagination

from notes import constant


def paginate(query_set, request):
    paginator = PageNumberPagination()
    paginator.page_size = constant.PAGE_SIZE
    result_page = paginator.paginate_queryset(query_set, request)
    return paginator, result_page
