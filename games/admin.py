from django.contrib import admin
from .models import Game, Focus, Material, Label, TrainingSession, SessionGame, GameSuggestion, Language, AboutContent


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']
    fields = ['code', 'name']


@admin.register(Focus)
class FocusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_languages_display']
    list_filter = ['languages']
    search_fields = ['name']
    filter_horizontal = ['languages']
    fields = ['name', 'description', 'languages']
    
    def get_languages_display(self, obj):
        return ', '.join([lang.name for lang in obj.languages.all()])
    get_languages_display.short_description = 'Languages'


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_languages_display']
    list_filter = ['languages']
    search_fields = ['name']
    filter_horizontal = ['languages']
    fields = ['name', 'description', 'languages']
    
    def get_languages_display(self, obj):
        return ', '.join([lang.name for lang in obj.languages.all()])
    get_languages_display.short_description = 'Languages'


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'get_languages_display']
    list_filter = ['languages']
    search_fields = ['name']
    filter_horizontal = ['languages']
    fields = ['name', 'color', 'languages']
    
    def get_languages_display(self, obj):
        return ', '.join([lang.name for lang in obj.languages.all()])
    get_languages_display.short_description = 'Languages'


class SessionGameInline(admin.TabularInline):
    model = SessionGame
    extra = 1
    fields = ['game', 'order', 'duration_multiplier', 'notes']


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_languages_display', 'created_by', 'created_at', 'get_total_duration']
    list_filter = ['languages', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['languages']
    fields = ['name', 'description', 'languages', 'created_by']
    inlines = [SessionGameInline]
    
    def get_languages_display(self, obj):
        return ', '.join([lang.name for lang in obj.languages.all()])
    get_languages_display.short_description = 'Languages'
    
    def get_total_duration(self, obj):
        return f"{obj.get_total_duration()} minutes"
    get_total_duration.short_description = 'Total Duration'


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_languages_display', 'get_focus_display', 'player_count', 'duration', 'is_active', 'is_suggestion']
    list_filter = ['languages', 'focus', 'player_count', 'duration', 'is_active', 'is_suggestion', 'labels']
    search_fields = ['name', 'description']
    filter_horizontal = ['focus', 'materials', 'labels', 'languages']
    readonly_fields = ['created_at', 'updated_at']
    fields = [
        'name', 'languages', 'focus', 'description', 'player_count', 'variants', 
        'materials', 'duration', 'labels', 'is_active', 'created_by', 
        'suggested_by', 'is_suggestion', 'approved', 'created_at', 'updated_at'
    ]
    
    def get_focus_display(self, obj):
        return obj.get_focus_display()
    get_focus_display.short_description = 'Focus Areas'
    
    def get_languages_display(self, obj):
        return obj.get_languages_display()
    get_languages_display.short_description = 'Languages'


@admin.register(GameSuggestion)
class GameSuggestionAdmin(admin.ModelAdmin):
    list_display = ['game', 'get_languages_display', 'submitted_by', 'submitted_at', 'status']
    list_filter = ['status', 'submitted_at', 'game__languages']
    search_fields = ['game__name', 'submitted_by__username']
    readonly_fields = ['submitted_at']
    
    def get_languages_display(self, obj):
        return obj.game.get_languages_display()
    get_languages_display.short_description = 'Languages'
    
    def save_model(self, request, obj, form, change):
        if obj.status == 'approved':
            obj.game.is_suggestion = False
            obj.game.approved = True
            obj.game.save()
        super().save_model(request, obj, form, change)


@admin.register(AboutContent)
class AboutContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    fields = ['title', 'content', 'is_active', 'order', 'created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order', 'created_at') 