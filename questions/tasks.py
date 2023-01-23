from datetime import datetime
from django.utils import timezone
from celery import shared_task
from .models import  Question


#delete after expired date
@shared_task
def delete_file():
    foos = Question.objects.all()

    files = Question.objects.filter(expiration_date=timezone.now())
    for foo in foos:

        # If the expiration date is bigger than now delete it
        if foo.expiration_date < timezone.now():
            foo.delete()
            # log deletion
    return "completed deleting foos at {}".format(timezone.now())
   