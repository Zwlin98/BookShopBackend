from django.urls import path

from book.views import BookListView, BookCategoryView

urlpatterns = [
    path('list/', BookListView.as_view()),
    path('category/', BookCategoryView.as_view())
]
