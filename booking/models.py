from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import random

# This class creates the objects stored in the database


class Order(models.Model):
    # edit this if you want longer or shorter order numbers
    ORDER_NUMBER_LENGTH = 4

    # Fields from the JSON object created by the webpage
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    liuid = models.CharField(max_length=255)
    email = models.EmailField()
    main_ticket = models.IntegerField()
    secondary_ticket = models.CharField(max_length=255)
    groupname = models.CharField(max_length=255)
    phone1 = models.CharField(max_length=255)
    phone2 = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    order_successful = models.BooleanField(default=False)
    order_number = models.CharField(
        max_length=ORDER_NUMBER_LENGTH, unique=True)
    session_id = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    validation_count = models.IntegerField(default=0)
    cs_team_name = models.CharField(max_length=255, default="", blank=True)
    lol_team_name = models.CharField(max_length=255, default="", blank=True)
    chess_participant = models.BooleanField(default=False)
    tft_participant = models.BooleanField(default=False)

    # overloads the save function to randomize an order number
    def save(self, *args, **kwargs):
        while not self.order_number:
            order_number = str(random.randint(
                0, 10**self.ORDER_NUMBER_LENGTH-1)).zfill(self.ORDER_NUMBER_LENGTH)
            if not Order.objects.filter(order_number=order_number).exists():
                self.order_number = order_number
        super().save(*args, **kwargs)
