from django.shortcuts import render, redirect, HttpResponse
from home.models import Contact
from tickets.models import Ticket, TicketComment
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

@login_required(login_url='/home')
def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        contact = Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
        messages.success(request, 'Your issue is submitted.!!')
        return redirect('contact')
    return render(request, 'home/contact.html')

@login_required
def aboutPage(request):
    return render(request, 'home/aboutPage.html')

@login_required
def search(request):
    query = request.GET['query']
    if len(query) > 78 or len(query) < 1:
        allTickets = Ticket.objects.none()
    else:
        allTitle = Ticket.objects.filter(title__contains=query)
        allContent = Ticket.objects.filter(content__contains=query)
        #ticketComments = TicketComment.objects.filter(comment__contains=query)
        allTickets = allTitle.union(allContent)
        # allTickets = Ticket.objects.all()
    if allTickets.count() == 0:
        messages.warning(request, "Query returned zero results")
    params = { "allTickets": allTickets, "query" : query }
    return render(request, 'home/search.html', params)

def signupAct(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if len(username) > 12:
            messages.warning(request, "Username must be maximum of 12 characters")
            return redirect('home')

        if not username.isalnum():
            messages.warning(request, "Username should contain Letters and Numbers")
            return redirect('home')

        if User.objects.filter(username=username).exists():
            messages.warning(request,'Username is taken. Try dfiffferent')
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.warning(request,'email-id is taken')
            return redirect('home')

        if password1 == password2:
            newUser = User.objects.create_user(username, email, password1)
            newUser.first_name = fname
            newUser.last_name = lname
            newUser.save()
            messages.success(request, "Your account has been created sucessfully!!")
        else:
            messages.warning(request, "Passwords don't match.")
        return redirect('home')
    else:
        return HttpResponse('''<h1> 404 - Page not found</h1> <a href="/"> Go to home</a>''')


def loginAct(request):
    if request.method == "POST":
        loginuser = request.POST['loginuser']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginuser, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, "login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('home')
    else:
        return HttpResponse('''<h1> 404 - Page not found</h1> <a href="/"> Go to home</a>''')

@login_required
def logoutAct(request):
    logout(request)
    messages.success(request, "Logout successful!")
    return redirect('home')
