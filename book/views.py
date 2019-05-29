from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from book.filter import BookFilter
from book.models import Book
from book.serializers import BookSerializer


class BookListView(ListAPIView):
    """
    书籍列表
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = BookFilter
    search_fields = ('name', 'category', 'description', 'author', 'year', 'pages', 'ISBN', 'language')


class BookCategoryView(APIView):
    """
    书籍分类信息
    """

    def get(self, requset):
        books = Book.objects.all()
        cate_list = set()
        for book in books:
            if book.category:
                cate_list.add(book.category)
        return Response(cate_list)
