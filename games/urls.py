from django.urls import path
from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/print/', views.print_session_builder, name='print_session_builder'),
    path('sessions/', views.session_list, name='session_list'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    path('suggest/', views.game_suggestion, name='game_suggestion'),
    path('print/game/<int:game_id>/', views.print_game, name='print_game'),
    path('print/session/<int:session_id>/', views.print_session, name='print_session'),
    path('set-language/', views.set_language, name='set_language'),
] 