from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Image,UserEvent

from events.models import UserEvent
@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_home(request):
    return render(request, 'admin_home.html')
def instructionsadmin(request):
    return render(request, 'instructionsadmin.html')


from .forms import UserEventForm
from events.models import Event

def home(request):

    us = Us.objects.last()

    return render(request, 'home.html', {'us': us})


def registered_events(request):
    user_events = UserEvent.objects.filter( registered=True)
    return render(request, 'registered_events.html', {'user_events': user_events})

def about(request):
    return render(request,'about.html')

def index(request):
    data = Image.objects.all()
    context = {
        'data' : data
    }
    return render(request,"admindisplay.html", context)


from .models import Event

#def events(request):
 #   events = Event.objects.all()
  #  return render(request, 'events.html', {'events': events})
#def add_event(request):
 #   if request.method == 'POST':
  #      event_name = request.POST['event_name']
   #     Event.objects.create(name=event_name)
    #return redirect('events')

#def remove_event(request, event_id):
#    event = Event.objects.get(id=event_id)
#    if request.method == 'POST':
#        event.delete()
#    return redirect('events')



from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')  # Redirect to admin home page
            else:
                return redirect('home')  # Redirect to regular user home page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


from .models import Us

from .forms import UserForm
def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to the profile page after form submission
    else:
        form = UserForm()

    return render(request, 'user_form.html', {'form': form})


def adminlogin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('adminhome')
        else:
            return render(request, 'adminlogin.html', {'error': 'Invalid credentials'})
    return render(request, 'adminlogin.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('login')
    return render(request, 'signup.html')


def sign(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('login')
    return render(request, 'signup.html')




def enter_event(request):
    if request.method == 'POST':
        event_id = request.POST['event_id']
        event_name = request.POST['event_name']
        event_venue = request.POST['event_venue']
        event_start_time = request.POST['event_start_time']
        event_end_time = request.POST['event_end_time']
        event_end_time = request.POST['event_end_time']
        event = Event(event_id=event_id, event_name=event_name, event_venue=event_venue, event_start_time=event_start_time, event_end_time=event_end_time)
        event.save()
        return redirect('admindisplay_events')
    return render(request, 'index.html')

def display_events(request):
    events = Event.objects.all()

    return render(request, 'display.html', {'events': events})
def admindisplay_events(request):
    events = Event.objects.all()
    return render(request, 'admindisplay.html', {'events': events})


def delete_event(request, event_id):
    event = Event.objects.get(event_id=event_id)
    event.delete()
    return redirect('display_events')

def logged_in_users(request):
    users = User.objects.all()
    return render(request, 'logged_in_users.html', {'users': users})



from .models import Class
from .forms import ClassForm

def class_list(request):
    classes = Class.objects.all()
    return render(request, 'class_list.html', {'classes': classes})

def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = ClassForm()

    return render(request, 'add_class.html', {'form': form})


from .models import Event, UserEvent
from .forms import UserEventForm

def register_event(request):
    if request.method == 'POST':
        form = UserEventForm(request.POST)
        if form.is_valid():
            event = form.cleaned_data['event']
            UserEvent.objects.create(user=request.user, event=event, registered=True)
            return redirect('register_event')

    form = UserEventForm()
    events = Event.objects.all()
    user_events = UserEvent.objects.filter(user=request.user)

    context = {

        'form': form,
        'events': events,
        'user_events': user_events,
    }

    return render(request, 'register.html', context)

def tts(request):
    return render(request, 'tts.html')


from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import UserEvent

def registered_events_next_day(request):
    # Get the current date and time
    now = timezone.now()

    # Calculate the start and end times for tomorrow
    tomorrow_start = now + timedelta(days=0)
    tomorrow_end = tomorrow_start + timedelta(days=1)

    # Filter UserEvent objects where the user is registered for events happening tomorrow
    user_events_next_day = UserEvent.objects.filter(
        user=request.user,
        event__event_start_time__gte=tomorrow_start,
        event__event_start_time__lt=tomorrow_end,
        registered=True
    )

    context = {
        'user_events_next_day': user_events_next_day,
    }

    return render(request, 'registered_events_next_day.html', context)



def create_or_update_profile(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        branch = request.POST.get('branch')
        year = request.POST.get('year')
        section = request.POST.get('section')
        university = request.POST.get('university')

        Us.objects.update_or_create(user=request.user, defaults={

            'gender': gender,
            'age': age,
            'branch': branch,
            'year': year,
            'section': section,
            'university': university,
        })

        return redirect('profile')  # Redirect to the profile page after saving

    return render(request, 'user_form.html')  # Render form for GET requests

def profile(request):
    us = Us.objects.filter(user=request.user).first()  # Get the profile for the logged-in user
    return render(request, 'profile.html', {'us': us})

