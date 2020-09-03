from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime

# Create your models here.
class Ticket(models.Model):
    tno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Assigned')
    slug = models.CharField(max_length=130)   
    timestamp = models.DateTimeField(default=now)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title + ' | Worked upon by : ' + self.author + ' |  Status: ' + self.status

class TicketComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return "Ticket No. " + str(self.ticket.tno) + " -  " + self.comment[0:13] + "..." + ' by ' + self.user.username + ' at ' + self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
    
class TicketAttachment(models.Model):
    sno = models.AutoField(primary_key=True)
    # attachment = models.FileField(upload_to='documents/%Y/%m/%d')
    attachment = models.URLField()   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return "Ticket No. " + str(self.ticket.tno) + " has an attachment " + str(self.attachment) + "..." + ' by ' + self.user.username + ' at ' + self.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
    