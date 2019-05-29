from django.urls import path

from announcement.views import AnnouncementListView

urlpatterns = [
    path('', AnnouncementListView.as_view()),
]
