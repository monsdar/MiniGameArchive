from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.conf import settings
import json
from django.views.decorators.http import require_http_methods
from django.utils import translation
from django.urls import reverse
from django.utils.translation import gettext as _
import logging

from .models import Game, Focus, Material, Label, TrainingSession, SessionGame, Language
from .forms import GameSuggestionForm, TrainingSessionForm

# Get logger for this module
logger = logging.getLogger(__name__)


def game_list(request):
    """Main page with game filtering and search"""
    games = Game.objects.filter(is_active=True, is_suggestion=False)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        games = games.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(variants__icontains=search_query)
        )
    
    # Filter by focus
    focus_filter = request.GET.getlist('focus')
    if focus_filter:
        games = games.filter(focus__name__in=focus_filter)
    
    # Filter by player count
    player_count = request.GET.get('player_count')
    if player_count:
        games = games.filter(player_count=player_count)
    
    # Filter by duration
    duration = request.GET.get('duration')
    if duration:
        games = games.filter(duration=duration)
    
    # Filter by materials
    materials_filter = request.GET.getlist('materials')
    if materials_filter:
        games = games.filter(materials__name__in=materials_filter)
    
    # Filter by labels
    labels_filter = request.GET.getlist('labels')
    if labels_filter:
        games = games.filter(labels__name__in=labels_filter)
    
    # Filter by languages
    languages_filter = request.GET.getlist('languages')
    if languages_filter:
        games = games.filter(languages__name__in=languages_filter)
    
    # Remove duplicates from many-to-many relationships
    games = games.distinct()
    
    # Pagination
    paginator = Paginator(games, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get filter options
    focuses = Focus.objects.all()
    materials = Material.objects.all()
    labels = Label.objects.all()
    languages = Language.objects.all()
    player_counts = Game.PLAYER_COUNT_CHOICES
    durations = Game.DURATION_CHOICES
    
    # Get training session from session
    cart = request.session.get('cart', [])
    cart_games = Game.objects.filter(id__in=cart)
    
    context = {
        'page_obj': page_obj,
        'focuses': focuses,
        'materials': materials,
        'labels': labels,
        'languages': languages,
        'player_counts': player_counts,
        'durations': durations,
        'search_query': search_query,
        'cart_games': cart_games,
        'cart_count': len(cart),
    }
    
    return render(request, 'games/game_list.html', context)


def game_detail(request, game_id):
    """Game detail page"""
    game = get_object_or_404(Game, id=game_id, is_active=True)
    
    # Check if game is in training session
    cart = request.session.get('cart', [])
    in_cart = game.id in cart
    
    context = {
        'game': game,
        'in_cart': in_cart,
    }
    
    return render(request, 'games/game_detail.html', context)


@require_http_methods(["POST"])
def add_to_cart(request):
    """Add game to training session"""
    try:
        data = json.loads(request.body)
        game_id = data.get('game_id')
        
        if not game_id:
            logger.warning("Add to cart failed: No game ID provided")
            return JsonResponse({'success': False, 'message': _('Game ID is required')})
        
        try:
            game = Game.objects.get(id=game_id)
            logger.debug(f"Adding game '{game.name}' (ID: {game_id}) to training session")
        except Game.DoesNotExist:
            logger.warning(f"Add to cart failed: Game with ID {game_id} not found")
            return JsonResponse({'success': False, 'message': _('Game not found')})
        
        cart = request.session.get('cart', [])
        if game_id not in cart:
            cart.append(game_id)
            request.session['cart'] = cart
            request.session.modified = True
            logger.info(f"Game '{game.name}' (ID: {game_id}) added to training session. Cart now has {len(cart)} items")
        else:
            logger.debug(f"Game '{game.name}' (ID: {game_id}) already in training session")
        
        return JsonResponse({
            'success': True, 
            'message': _('Game added to training session'),
            'cart_count': len(cart)
        })
        
    except json.JSONDecodeError as e:
        logger.error(f"Add to cart failed: Invalid JSON data - {e}")
        return JsonResponse({'success': False, 'message': _('Invalid JSON data')})
    except Exception as e:
        logger.error(f"Add to cart failed: Unexpected error - {e}")
        return JsonResponse({'success': False, 'message': str(e)})


@require_http_methods(["POST"])
def remove_from_cart(request):
    """Remove game from training session"""
    try:
        data = json.loads(request.body)
        game_id = data.get('game_id')
        
        if not game_id:
            logger.warning("Remove from cart failed: No game ID provided")
            return JsonResponse({'success': False, 'message': _('Game ID is required')})
        
        cart = request.session.get('cart', [])
        if game_id in cart:
            try:
                game = Game.objects.get(id=game_id)
                logger.info(f"Removing game '{game.name}' (ID: {game_id}) from training session")
            except Game.DoesNotExist:
                logger.warning(f"Remove from cart: Game with ID {game_id} not found in database")
            
            cart.remove(game_id)
            request.session['cart'] = cart
            request.session.modified = True
            logger.debug(f"Game (ID: {game_id}) removed from training session. Cart now has {len(cart)} items")
        else:
            logger.debug(f"Game (ID: {game_id}) not found in training session")
        
        return JsonResponse({
            'success': True, 
            'message': _('Game removed from training session'),
            'cart_count': len(cart)
        })
        
    except json.JSONDecodeError as e:
        logger.error(f"Remove from cart failed: Invalid JSON data - {e}")
        return JsonResponse({'success': False, 'message': _('Invalid JSON data')})
    except Exception as e:
        logger.error(f"Remove from cart failed: Unexpected error - {e}")
        return JsonResponse({'success': False, 'message': str(e)})


def cart_view(request):
    """View training session contents"""
    cart = request.session.get('cart', [])
    cart_games = Game.objects.filter(id__in=cart)
    
    logger.debug(f"Cart view accessed with {len(cart)} games in session")
    
    # Calculate total duration
    total_duration = 0
    for game in cart_games:
        duration_str = game.duration
        if '+' in duration_str:
            # For ranges like "10+min", use the minimum
            minutes = int(duration_str.replace('+min', ''))
        else:
            minutes = int(duration_str.replace('min', ''))
        total_duration += minutes
    
    logger.debug(f"Calculated total duration: {total_duration} minutes")
    
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.created_by = request.user
            session.save()
            
            logger.info(f"Creating training session '{session.name}' with {len(cart)} games")
            
            # Add games to session
            for i, game_id in enumerate(cart):
                game = Game.objects.get(id=game_id)
                SessionGame.objects.create(
                    session=session,
                    game=game,
                    order=i + 1
                )
                logger.debug(f"Added game '{game.name}' to session '{session.name}' at position {i + 1}")
            
            # Clear training session
            request.session['cart'] = []
            request.session.modified = True
            
            messages.success(request, _('Training session "%(name)s" created successfully!') % {'name': session.name})
            logger.info(f"Training session '{session.name}' created successfully by user {request.user.username}")
            return redirect('session_detail', session_id=session.id)
        else:
            logger.warning(f"Training session form validation failed: {form.errors}")
    else:
        form = TrainingSessionForm()
    
    context = {
        'cart_games': cart_games,
        'form': form,
        'total_duration': total_duration,
    }
    
    return render(request, 'games/cart.html', context)


def print_session_builder(request):
    """Print a training session directly from the builder without saving"""
    cart = request.session.get('cart', [])
    cart_games = Game.objects.filter(id__in=cart)
    
    if not cart_games:
        messages.error(request, 'No games in your training session to print.')
        return redirect('cart')
    
    # Create a temporary session object for printing
    class TempSessionGame:
        def __init__(self, game, order):
            self.game = game
            self.order = order
            self.duration_multiplier = 1.0
            self.notes = ''
    
    class TempSession:
        def __init__(self, games):
            self.name = 'Training Session'
            self.description = ''
            self.created_at = None
            self._games = games
        
        def get_total_duration(self):
            total_minutes = 0
            for session_game in self.sessiongame_set.all():
                duration_str = session_game.game.duration
                if '+' in duration_str:
                    minutes = int(duration_str.replace('+min', ''))
                else:
                    minutes = int(duration_str.replace('min', ''))
                total_minutes += minutes * session_game.duration_multiplier
            return total_minutes
        
        @property
        def sessiongame_set(self):
            class TempSessionGameSet:
                def __init__(self, games):
                    self._games = games
                
                def all(self):
                    return [TempSessionGame(game, i + 1) for i, game in enumerate(self._games)]
            
            return TempSessionGameSet(self._games)
    
    temp_session = TempSession(cart_games)
    
    context = {
        'session': temp_session,
    }
    
    html = render_to_string('games/print_session.html', context)
    
    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="training_session.html"'
    response.write(html)
    
    return response


@login_required
def session_detail(request, session_id):
    """Training session detail page"""
    session = get_object_or_404(TrainingSession, id=session_id, created_by=request.user)
    
    context = {
        'session': session,
    }
    
    return render(request, 'games/session_detail.html', context)


@login_required
def session_list(request):
    """List user's training sessions"""
    sessions = TrainingSession.objects.filter(created_by=request.user)
    
    context = {
        'sessions': sessions,
    }
    
    return render(request, 'games/session_list.html', context)


def game_suggestion(request):
    """Submit a new game suggestion"""
    if request.method == 'POST':
        form = GameSuggestionForm(request.POST)
        if form.is_valid():
            game = form.save(user=request.user)
            messages.success(request, 'Game suggestion submitted successfully! It will be reviewed by an admin.')
            return redirect('game_list')
        else:
            print(f"GameSuggestionForm errors: {form.errors}")
    else:
        form = GameSuggestionForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'games/game_suggestion.html', context)


def print_game(request, game_id):
    """Print a single game card"""
    game = get_object_or_404(Game, id=game_id, is_active=True)
    
    context = {
        'game': game,
    }
    
    html = render_to_string('games/print_game.html', context)
    
    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="game_{game.id}.html"'
    response.write(html)
    
    return response


def print_session(request, session_id):
    """Print a training session"""
    session = get_object_or_404(TrainingSession, id=session_id)
    
    context = {
        'session': session,
    }
    
    html = render_to_string('games/print_session.html', context)
    
    response = HttpResponse(content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="session_{session.id}.html"'
    response.write(html)
    
    return response


@require_http_methods(["POST"])
def clear_cart(request):
    """Clear all games from training session"""
    cart = request.session.get('cart', [])
    if cart:
        logger.info(f"Clearing training session with {len(cart)} games")
    else:
        logger.debug("Clearing empty training session")
    
    request.session['cart'] = []
    request.session.modified = True
    messages.success(request, _('Training session cleared successfully!'))
    return redirect('cart')


def set_language(request):
    """Set user language preference in session"""
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            logger.info(f"User changing language to: {language}")
            # Store language preference in session
            request.session['django_language'] = language
            request.session.modified = True
            
            # Set language for current request
            translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
        else:
            logger.warning("Language change attempted but no language specified")
    
    # Redirect back to the page they came from
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    logger.debug(f"Redirecting to: {next_url}")
    return HttpResponseRedirect(next_url)