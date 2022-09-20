from django_filters import rest_framework as filters


class NotesFilter(filters.FilterSet):
    shared = filters.BooleanFilter(method="shared_filter")

    def shared_filter(self, queryset, name, value):
        if value:
            queryset = self.queryset.filter(shared_with=self.request.user)
            return queryset

        queryset = self.queryset.filter(user=self.request.user)
        return queryset
