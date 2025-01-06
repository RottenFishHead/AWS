from django.contrib import admin
from .models import PokerSession, Casino, Tag, SessionNotes

@admin.register(PokerSession)
class PokerSessionAdmin(admin.ModelAdmin):
    list_display = ['player', 'casino', 'stakes', 'hours', 'buy_in', 'cash_out']
    list_filter = ['player', 'casino', ]
    search_fields = ['player__username', 'casino__name']
    date_hierarchy = 'date'
    ordering = [ 'date']

@admin.register(Casino)
class CasinoAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(SessionNotes)
class SessionNotesAdmin(admin.ModelAdmin):
    list_display = ['notes', 'tags', 'takeaway']
    search_fields = ['tags']