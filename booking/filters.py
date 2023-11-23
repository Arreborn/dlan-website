from django.contrib.admin import SimpleListFilter


class NonEmptyCsTeamNameFilter(SimpleListFilter):
    title = 'CS Team Name'  # Human-readable title for the filter
    parameter_name = 'cs_team_name'  # URL query parameter for the filter

    def lookups(self, request, model_admin):
        return (
            ('non_empty', 'Non-empty'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'non_empty':
            return queryset.exclude(cs_team_name="")
        return queryset


class NonEmptyLolTeamNameFilter(SimpleListFilter):
    title = 'LoL Team Name'  # Human-readable title for the filter
    parameter_name = 'lol_team_name'  # URL query parameter for the filter

    def lookups(self, request, model_admin):
        return (
            ('non_empty', 'Non-empty'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'non_empty':
            return queryset.exclude(lol_team_name="")
        return queryset
