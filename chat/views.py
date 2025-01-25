from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Contact, Message


# Signup view
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Login view
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')


# Dashboard view
@login_required
def dashboard(request):
    search_query = request.GET.get('search', '')
    search_results = []
    if search_query:
        search_results = User.objects.filter(
            Q(username__icontains=search_query) & ~Q(username=request.user.username)
        )

    contacts = Contact.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {
        'contacts': contacts,
        'search_results': search_results,
        'search_query': search_query
    })


# Add Contact view
@login_required
def add_contact(request, contact_username):
    contact_user = get_object_or_404(User, username=contact_username)
    if contact_user != request.user:
        Contact.objects.get_or_create(user=request.user, contact_user=contact_user)
        Contact.objects.get_or_create(user=contact_user, contact_user=request.user)
    return redirect('dashboard')


# Chat view
@login_required
def chat_view(request, contact_username):
    contact_user = get_object_or_404(User, username=contact_username)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=contact_user) |
        Q(sender=contact_user, recipient=request.user)
    ).order_by('timestamp')
    return render(request, 'chat.html', {
        'contact_user': contact_user,
        'messages': messages
    })
