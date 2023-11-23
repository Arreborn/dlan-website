from django.contrib.admin import SimpleListFilter
from django.contrib import admin
from .models import Order
from .filters import NonEmptyCsTeamNameFilter, NonEmptyLolTeamNameFilter


class TicketFilter(SimpleListFilter):
    title = 'Ticket Filter'
    parameter_name = 'ticket_filter'

    def lookups(self, request, model_admin):
        return (
            ('main_ticket', 'Main Ticket is 2'),
            ('secondary_ticket', 'Secondary Ticket is 2'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'main_ticket':
            return queryset.filter(main_ticket=2)
        elif self.value() == 'secondary_ticket':
            return queryset.filter(secondary_ticket=2)


class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'

    def cs_team_name_display(self, obj):
        return obj.cs_team_name if obj.cs_team_name else ''
    cs_team_name_display.short_description = 'CS Team Name'

    def lol_team_name_display(self, obj):
        return obj.lol_team_name if obj.lol_team_name else ''
    lol_team_name_display.short_description = 'LoL Team Name'

    list_display = ('order_number', 'fname', 'lname', 'liuid', 'groupname', 'main_ticket', 'secondary_ticket',
                    'validation_count', 'cs_team_name_display', 'lol_team_name_display', 'tft_participant', 'chess_participant', 'date_created')
    list_editable = ('validation_count', )
    search_fields = ('order_number', 'fname', 'lname', 'email', 'groupname',
                     'liuid', 'cs_team_name', 'lol_team_name')
    list_filter = ('tft_participant', 'chess_participant', NonEmptyCsTeamNameFilter,
                   NonEmptyLolTeamNameFilter, TicketFilter,)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Order Validators').exists():
            if obj:  # Editing an existing object
                fields = [f.name for f in self.model._meta.fields if f.name not in [
                    'validation_count', 'cs_team_name', 'lol_team_name', 'chess_participant', 'tft_participant']]
            else:  # Creating a new object
                fields = []
            return fields
        return super().get_readonly_fields(request, obj)


admin.site.register(Order, OrderAdmin)
