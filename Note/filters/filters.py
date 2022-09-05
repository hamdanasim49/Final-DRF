from Note.models import Note
from django_filters import FilterSet, BooleanFilter, CharFilter


class NotesArchiveFilter(FilterSet):

    title = CharFilter(
        lookup_expr="iexact",
    )

    class Meta:
        model = Note
        fields = ["archive", "title"]
