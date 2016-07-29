from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse

from .models import Treasure #, HashTag
from .forms import TreasureForm, LoginForm

def index(request):
    treasures = Treasure.objects.all()
    form = TreasureForm()
    return render(request, 'index.html', {'treasures': treasures, 'form':form})

def post_treasure(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TreasureForm(data = request.POST, files = request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            treasure = form.save(commit = False)
            treasure.user = request.user
            treasure.likes = 0
            treasure.save()
        # redirect to a new URL:
        return HttpResponseRedirect('/')

def detail(request, treasure_id):
    treasure = Treasure.objects.get(id=treasure_id)
    #hashtags = HashTag.objects.filter(treasure=treasure_id)
    return render(request, 'detail.html',
                  {'treasure': treasure})

def profile(request, username):
    user = get_object_or_404(User.objects, username=username)
    treasures = Treasure.objects.filter(user=user)
    return render(request, 'profile.html', {'username':username,'treasures': treasures})


def like_treasure(request):
    treasure_id = request.POST.get('treasure_id', None)

    likes = 0
    if (treasure_id):
        treasure = Treasure.objects.get(id=int(treasure_id))
        if treasure is not None:
            likes = treasure.likes + 1
            treasure.likes = likes
            treasure.save()

    return HttpResponse(likes)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                # the password verified for the user
                if user.is_active:
                    print("User is valid, active and authenticated")
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The password is valid, but the account has been disabled!")
            else:
                # the authentication system was unable to verify the username and password
                print("The username and password were incorrect.")

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
