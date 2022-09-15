from django_filters import BooleanFilter
from django_filters import CharFilter
from django_filters import FilterSet
from django_filters import rest_framework as rest_filters

from notes.models import Note


class NotesShareFilter(rest_filters.FilterSet):
    is_shared = BooleanFilter(name="shared_with", method="filter_is_shared")

    class Meta:
        model = Note
        fields = [
            "shared_with",
        ]

    def filter_is_shared(self, queryset, name, value):
        return queryset
