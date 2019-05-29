from rest_framework.generics import ListAPIView

from announcement.models import Announcement
from announcement.serializers import AnnouncementSerializer


class AnnouncementListView(ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
