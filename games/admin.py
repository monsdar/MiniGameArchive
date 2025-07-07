from django.contrib import admin
from .models import Game, Focus, Material, Label, TrainingSession, SessionGame, GameSuggestion


@admin.register(Focus)
class FocusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'language']
    list_filter = ['language']
    search_fields = ['name']
    fields = ['name', 'description', 'language']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'language']
    list_filter = ['language']
    search_fields = ['name']
    fields = ['name', 'description', 'language']


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'language']
    list_filter = ['language']
    search_fields = ['name']
    fields = ['name', 'color', 'language']


class SessionGameInline(admin.TabularInline):
    model = SessionGame
    extra = 1
    fields = ['game', 'order', 'duration_multiplier', 'notes']


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'language', 'created_by', 'created_at', 'get_total_duration']
    list_filter = ['language', 'created_at']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'language', 'created_by']
    inlines = [SessionGameInline]
    
    def get_total_duration(self, obj):
        return f"{obj.get_total_duration()} minutes"
    get_total_duration.short_description = 'Total Duration'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'language', 'get_focus_display', 'player_count', 'duration', 'is_active', 'is_suggestion']
    list_filter = ['language', 'focus', 'player_count', 'duration', 'is_active', 'is_suggestion', 'labels']
    search_fields = ['name', 'description']
    filter_horizontal = ['focus', 'materials', 'labels']
    readonly_fields = ['created_at', 'updated_at']
    fields = [
        'name', 'language', 'focus', 'description', 'player_count', 'variants', 
        'materials', 'duration', 'labels', 'is_active', 'created_by', 
        'suggested_by', 'is_suggestion', 'approved', 'created_at', 'updated_at'
    ]
    
    def get_focus_display(self, obj):
        return obj.get_focus_display()
    get_focus_display.short_description = 'Focus Areas'


@admin.register(GameSuggestion)
class GameSuggestionAdmin(admin.ModelAdmin):
    list_display = ['game', 'language', 'submitted_by', 'submitted_at', 'status']
    list_filter = ['status', 'submitted_at', 'game__language']
    search_fields = ['game__name', 'submitted_by__username']
    readonly_fields = ['submitted_at']
    
    def language(self, obj):
        return obj.game.language
    language.short_description = 'Language'
    
    def save_model(self, request, obj, form, change):
        if obj.status == 'approved':
            obj.game.is_suggestion = False
            obj.game.approved = True
            obj.game.save()
        super().save_model(request, obj, form, change) 