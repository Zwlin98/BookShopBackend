from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        # fields = '__all__'
        exclude = (
            'download_link_pdf',
            'download_link_epub',
            'add_time'
        )
