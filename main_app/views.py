from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Game, Char, Photo
from .forms import PlayingForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'videogamecollector'

# Create your views here.


# Add the following import




# Define the home view
def home(request):
  return render(request, 'home.html' )

def about(request): 
    return render(request, 'about.html')

@login_required
def games_index(request):
    games = Game.objects.filter(user=request.user)
    return render(request, 'games/index.html', {'games' : games})

@login_required
def games_detail(request, game_id):
  game = Game.objects.get(id=game_id)
  chars_game_doesnt_have = Char.objects.exclude(id__in = game.chars.all().values_list('id'))
  playing_form = PlayingForm()
  return render(request, 'games/detail.html', { 
    'game': game, 'playing_form': playing_form,
    'chars' : chars_game_doesnt_have 
    
    })

@login_required
def add_playing(request, game_id):
  # create the ModelForm using the data in request.POST
  form = PlayingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it
    # has the game_id assigned
    new_playing = form.save(commit=False)
    new_playing.game_id = game_id
    new_playing.save()
  return redirect('detail', game_id=game_id)

@login_required
def assoc_char(request, game_id, char_id):
  # Note that you can pass a char's id instead of the whole object
  Game.objects.get(id=game_id).chars.add(char_id)
  return redirect('detail', game_id=game_id)

@login_required
def add_photo(request, game_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to game_id or game (if you have a game object)
            photo = Photo(url=url, game_id=game_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', game_id=game_id)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class GameCreate(LoginRequiredMixin, CreateView):
  model = Game
  fields = ['name', 'genre', 'description', 'age']
 
  # This inherited method is called when a
  # valid game form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user
    # Let the CreateView do its job as usual
    return super().form_valid(form)
  

class GameUpdate(LoginRequiredMixin, UpdateView):
  model = Game
  # Let's disallow the renaming of a game by excluding the name field!
  fields = ['genre', 'description', 'age']

class GameDelete(LoginRequiredMixin, DeleteView):
  model = Game
  success_url = '/games/'

class CharList(LoginRequiredMixin, ListView):
  model = Char

class CharDetail(LoginRequiredMixin, DetailView):
  model = Char

class CharCreate(LoginRequiredMixin, CreateView):
  model = Char
  fields = '__all__'

class CharUpdate(LoginRequiredMixin, UpdateView):
  model = Char
  fields = ['name', 'color']

class CharDelete(LoginRequiredMixin, DeleteView):
  model = Char
  success_url = '/chars/'