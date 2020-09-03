from django.contrib import admin
from django.urls import path, include
from tickets import views

urlpatterns = [
    path('ticketAttachments', views.ticketAttachments, name='ticketAttachments'),
    path('ticketComments', views.ticketComments, name='ticketComments'),
    path('deleteAttachment', views.deleteAttachment, name='deleteAttachment'),
    path('deleteComment', views.deleteComment, name='deleteComment'),
    path('editComment', views.editComment, name='editComment'),
    path('deleteTicket', views.deleteTicket, name='deleteTicket'),
    path('', views.ticketsHome, name='ticketsHome'),
    path('createTicket', views.createTicket, name='createTicket'),
    path('editTicket', views.editTicket, name='editTicket'),
    # path('<str:slug>', views.ticketDetails, name='ticketDetails'),
    path('myTickets', views.myTickets, name='myTickets'),
    path('<str:tno>', views.ticketDetails, name='ticketDetails'),
]