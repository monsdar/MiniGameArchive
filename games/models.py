from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import get_language


class Language(models.Model):
    """Languages supported by the application"""
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Focus(models.Model):
    """Focus areas for games (e.g., Dribbling, Teamwork, Layups)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    languages = models.ManyToManyField(Language, related_name='focus_areas')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_languages_display(self):
        return ', '.join([lang.name for lang in self.languages.all()])


class Material(models.Model):
    """Materials needed for games (e.g., Basketball, Halfcourt, Hoop)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    languages = models.ManyToManyField(Language, related_name='materials')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_languages_display(self):
        return ', '.join([lang.name for lang in self.languages.all()])


class Label(models.Model):
    """Custom labels for categorizing games"""
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color
    languages = models.ManyToManyField(Language, related_name='labels')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_languages_display(self):
        return ', '.join([lang.name for lang in self.languages.all()])


class Game(models.Model):
    """A game or exercise for sports training"""
    DURATION_CHOICES = [
        ('5min', '5 minutes'),
        ('15min', '15 minutes'),
        ('30min', '30 minutes'),
        ('45min', '45 minutes'),
        ('60min', '60 minutes'),
    ]
    
    PLAYER_COUNT_CHOICES = [
        ('1', '1 player'),
        ('2', '2 players'),
        ('3+', '3+ players'),
        ('5+', '5+ players'),
        ('10+', '10+ players'),
        ('15+', '15+ players'),
        ('any', 'Any number'),
    ]
    
    name = models.CharField(max_length=200)
    focus = models.ManyToManyField(Focus, related_name='games')
    description = models.TextField()
    player_count = models.CharField(max_length=10, choices=PLAYER_COUNT_CHOICES)
    variants = models.TextField(blank=True)
    materials = models.ManyToManyField(Material, related_name='games', blank=True)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    labels = models.ManyToManyField(Label, related_name='games', blank=True)
    languages = models.ManyToManyField(Language, related_name='games')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_games')
    
    # User suggestions
    suggested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_suggestion = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def get_focus_display(self):
        return ', '.join([focus.name for focus in self.focus.all()])
    
    def get_materials_display(self):
        return ', '.join([material.name for material in self.materials.all()])
    
    def get_labels_display(self):
        return ', '.join([label.name for label in self.labels.all()])
    
    def get_languages_display(self):
        return ', '.join([lang.name for lang in self.languages.all()])


class TrainingSession(models.Model):
    """A training session containing multiple games"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    games = models.ManyToManyField(Game, through='SessionGame', related_name='training_sessions')
    languages = models.ManyToManyField(Language, related_name='training_sessions')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def get_total_duration(self):
        """Calculate total duration of the session"""
        total_minutes = 0
        for session_game in self.sessiongame_set.all():
            duration_str = session_game.game.duration
            # All durations now end with 'min'
            minutes = int(duration_str.replace('min', ''))
            total_minutes += minutes * session_game.duration_multiplier
        return total_minutes


class SessionGame(models.Model):
    """Intermediate model for games in training sessions with order and duration"""
    session = models.ForeignKey(TrainingSession, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    duration_multiplier = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.5), MaxValueValidator(3.0)],
        help_text="Multiplier for game duration (0.5 = half time, 2.0 = double time)"
    )
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['order']
        unique_together = ['session', 'game', 'order']
    
    def __str__(self):
        return f"{self.session.name} - {self.game.name} (Order: {self.order})"


class AboutContent(models.Model):
    """Custom content for the About modal that admins can edit"""
    title = models.CharField(max_length=200, help_text="Title for the custom section")
    content = models.TextField(help_text="Content in markdown format")
    is_active = models.BooleanField(default=True, help_text="Whether this content should be displayed")
    order = models.PositiveIntegerField(default=0, help_text="Order of display in the About modal")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = "About Content"
        verbose_name_plural = "About Content"
    
    def __str__(self):
        return f"{self.title} ({'Active' if self.is_active else 'Inactive'})"


class GameSuggestion(models.Model):
    """Model for user suggestions of new games"""
    game = models.OneToOneField(Game, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    
    class Meta:
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"Suggestion: {self.game.name} by {self.submitted_by.username}" 