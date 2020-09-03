from django.contrib import admin
from tickets.models import Ticket, TicketComment, TicketAttachment

# Register your models here.
admin.site.register((Ticket, TicketComment, TicketAttachment))