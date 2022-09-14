from django_filters import BooleanFilter
from django_filters import CharFilter
from django_filters import FilterSet
from django_filters import rest_framework as rest_filters

from notes.models import Note


class NotesShareFilter(FilterSet):
    archive = BooleanFilter(method="filter_is_archive")
    print("In file filter***")

    class Meta:
        model = Note
        fields = [
            "archive",
        ]

    def filter_is_archive(self, queryset, name, value):
        print("Bro")
        if value:
            print("Allo", value)
            return queryset.filter(archive=True)
        else:
            return queryset.filter(archive=False)
