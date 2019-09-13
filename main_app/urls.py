from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('games/', views.games_index, name='index'),
    path('games/<int:game_id>/', views.games_detail, name='detail'),
      # new route used to show a form and create a game
    path('games/create/', views.GameCreate.as_view(), name='games_create'),
    path('games/<int:pk>/update/', views.GameUpdate.as_view(), name='games_update'),
    path('games/<int:pk>/delete/', views.GameDelete.as_view(), name='games_delete'),
    path('games/<int:game_id>/add_playing/', views.add_playing, name='add_playing'),
    path('games/<int:game_id>/assoc_char/<int:char_id>/', views.assoc_char, name='assoc_char'),
    path('games/<int:game_id>/add_photo/', views.add_photo, name='add_photo'),
    path('chars/', views.CharList.as_view(), name='chars_index'),
    path('chars/<int:pk>/', views.CharDetail.as_view(), name='chars_detail'),
    path('chars/create/', views.CharCreate.as_view(), name='chars_create'),
    path('chars/<int:pk>/update/', views.CharUpdate.as_view(), name='chars_update'),
    path('chars/<int:pk>/delete/', views.CharDelete.as_view(), name='chars_delete'),
    path('accounts/signup', views.signup, name='signup'),
]