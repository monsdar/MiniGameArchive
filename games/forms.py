from django import forms
from django.contrib.auth.models import User
from .models import Game, TrainingSession, GameSuggestion


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            'name', 'focus', 'description', 'player_count', 
            'variants', 'materials', 'duration', 'labels'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'variants': forms.Textarea(attrs={'rows': 3}),
        }


class GameSuggestionForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = [
            'name', 'focus', 'description', 'player_count', 
            'variants', 'materials', 'duration', 'labels'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'variants': forms.Textarea(attrs={'rows': 3}),
        }
    
    def save(self, user, commit=True):
        game = super().save(commit=False)
        game.suggested_by = user
        game.is_suggestion = True
        game.approved = False
        if commit:
            game.save()
            self.save_m2m()
            # Create GameSuggestion
            GameSuggestion.objects.create(game=game, submitted_by=user)
        return game


class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SessionGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = []  # This form is just for adding games to sessions
    
    game_id = forms.IntegerField(widget=forms.HiddenInput())
    duration_multiplier = forms.FloatField(
        min_value=0.5,
        max_value=3.0,
        initial=1.0,
        widget=forms.NumberInput(attrs={'step': 0.1, 'class': 'form-control'})
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'})
    ) 