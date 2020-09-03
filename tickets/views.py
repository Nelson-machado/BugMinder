from django.shortcuts import render, HttpResponse, redirect
from tickets.models import Ticket, TicketComment, TicketAttachment
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from datetime import date, timedelta, timezone
import datetime

# Create your views here.
@login_required
def ticketsHome(request):
    allTickets = Ticket.objects.all().order_by('-timestamp')
    context = {
        'allTickets': allTickets
    }
    return render(request, 'tickets/ticketsHome.html', context)

@login_required
def myTickets(request):
    selectedStatus = request.GET.get('status_dropdown')
    allTickets = Ticket.objects.filter(author__icontains=request.user).order_by('-timestamp')
    allTicketCount = allTickets.filter(author__icontains=request.user).count()
    assignedTicketCount = allTickets.filter(author__icontains=request.user, status__icontains='Assigned').count()
    inProgressTicketCount = allTickets.filter(author__icontains=request.user, status__icontains='inProgress').count()
    onHoldTicketCount = allTickets.filter(author__icontains=request.user, status__icontains='onHold').count()
    resolvedTicketCount = allTickets.filter(author__icontains=request.user, status__icontains='resolved').count()
    # print(selectedStatus)
    # print(allTickets)
    # today1 =  datetime.datetime.now(tz=timezone.utc) + timedelta(1)
    # print('todays date: ', today1.strftime("%m/%d/%Y, %H:%M:%S"))
    # diviatedTicket = allTickets.filter(end_date__lte=today1)
    # print(diviatedTicket)
    distinctStatus = Ticket.objects.values('status').distinct()
    distinctStatus = distinctStatus.filter(author__icontains=request.user)

    if selectedStatus != '' and selectedStatus is not None:
        allTickets = allTickets.filter(author__icontains=request.user, status__icontains=selectedStatus).order_by('-timestamp')
      
    elif selectedStatus is None:
        allTickets = Ticket.objects.filter(author__icontains=request.user).order_by('-timestamp')

    context = {
         'allTickets': allTickets,
         'distinctStatus': distinctStatus,
         'allTicketCount': allTicketCount,
         'assignedTicketCount': assignedTicketCount,
         'inProgressTicketCount': inProgressTicketCount,
         'onHoldTicketCount': onHoldTicketCount,
         'resolvedTicketCount': resolvedTicketCount,
         'selectedStatus': selectedStatus
        #  'diviatedTicket': diviatedTicket
    }

    return render(request, 'tickets/myTickets.html', context)

@login_required
def ticketDetails(request, tno):
    # ticket = Ticket.objects.filter(slug=slug).first()
    ticket = Ticket.objects.filter(tno=tno).first()
    comments = TicketComment.objects.filter(ticket=ticket)
    attachments = TicketAttachment.objects.filter(ticket=ticket)
    context = {
        'ticket': ticket,
        'comments': comments,
        'attachments': attachments
    }
    return render(request, 'tickets/ticketDetails.html', context)

@login_required
def ticketComments(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        ticketTno = request.POST.get('ticketTno')
        ticket = Ticket.objects.get(tno=ticketTno)

        comment = TicketComment(comment=comment, user=user, ticket=ticket)
        comment.save()
        messages.success(request, "Your comment has been added, successfully")

    return redirect(f'/tickets/{ticket.tno}')

@login_required
def ticketAttachments(request):
    if request.method == "POST" and request.FILES['attachment']:
        attachment = request.FILES['attachment']
        fs = FileSystemStorage()
        filename = fs.save(attachment.name, attachment)
        url = fs.url(filename)

        user = request.user
        ticketTno = request.POST.get('ticketTno')
        ticket = Ticket.objects.get(tno=ticketTno)

        saveAttachment = TicketAttachment(attachment=url, user=user, ticket=ticket)
        saveAttachment.save()
        messages.success(request, "Your file has been uploaded, successfully")

    return redirect(f'/tickets/{ticket.tno}')


@login_required
def createTicket(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        author = request.POST.get('author')
        ticket_save = Ticket(title=title, content=content, author=author)
        ticket_save.save()
        print("ticket created")
        last_saved_ticket= Ticket.objects.last()
        messages.success(request, f'Ticket: {last_saved_ticket.tno} has been created successfully!' )
    return redirect(f'/tickets/{last_saved_ticket.tno}')


@login_required
def editTicket(request):
    if request.method == "POST":
        tno = request.POST.get('tno')
        title = request.POST.get('title')
        content = request.POST.get('content')
        status = request.POST.get('status')
        end_date = request.POST.get('end_date')
        print('end_date', end_date)
        editedTicket = Ticket.objects.get(tno=tno)
        editedTicket.title = title
        editedTicket.content = content
        editedTicket.status = status

        if not(end_date == '') or (end_date is not None):
            editedTicket.end_date = end_date

        editedTicket.save()
        print("ticket updated")
        messages.success(request, f'Ticket: {editedTicket.tno} has been updated successfully!' )
    return redirect(f'/tickets/{editedTicket.tno}')

@login_required
def deleteAttachment(request):
    if request.method == "POST":
        attachment = request.POST.get('attachment')
        timestamp = request.POST.get('timestamp')
        sno = request.POST.get('sno')
        user = request.user
        ticketTno = request.POST.get('ticketTno')
        ticket = Ticket.objects.get(tno=ticketTno)
        delAttachment = TicketAttachment.objects.get(sno=sno, ticket=ticket, attachment=attachment, user=user )
        delAttachment.delete()
        messages.success(request, "Your file has been deleted, successfully")

    return redirect(f'/tickets/{ticket.tno}')

@login_required
def deleteComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        sno = request.POST.get('srno')
        user = request.user
        ticketTno = request.POST.get('ticketTno')
        ticket = Ticket.objects.get(tno=ticketTno)

        delcomment = TicketComment.objects.get(sno=sno, user=user, ticket=ticket)
        delcomment.delete()
        messages.success(request, "Your comment has been deleted, successfully")

    return redirect(f'/tickets/{ticket.tno}')
    

@login_required
def editComment(request):
    if request.method == "POST":
        comment2 = request.POST.get('editCommentId')
        sno = request.POST.get('scno')
        user = request.user
        ticketTno = request.POST.get('ticketTno')
        ticket = Ticket.objects.get(tno=ticketTno)

        editcomment = TicketComment.objects.get(sno=sno, user=user, ticket=ticket)
        editcomment.comment=comment2
        editcomment.save()
        messages.success(request, "Your comment has been edited, successfully")

    return redirect(f'/tickets/{ticket.tno}')

@login_required
def deleteTicket(request):
    if request.method == "POST":
        tno = request.POST.get('tno')
        delTicket = Ticket.objects.filter(tno=tno).first()
        print(delTicket)
        delTicket.delete()
        messages.success(request, f'Your  ticket has been deleted, successfully')

    return redirect('myTickets')