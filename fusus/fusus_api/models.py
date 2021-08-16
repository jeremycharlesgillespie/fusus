from django.db import models


class Organization(models.Model):
    """
    This class represents the Organization object in the database.
    """
    # id <-This is created by Django as the primary key, nothing to add here.
    name = models.CharField(max_length=50)  # Setting max_length to 50 to allow for long organization names.
    phone = models.CharField(max_length=20)  # Setting max_length to 20 to allow for international numbers.
    address = models.CharField(max_length=255)  # Ideally this would be broken into St Address 1, St Address 2, City,
    # State, Zip, etc.


class User(models.Model):
    """
    This class represents the User object in the database.
    """
    # id <-This is created by Django as the primary key, nothing to add here.
    name = models.CharField(max_length=50)  # Setting max_length to 50 to allow for First+Middle+Last names. Ideally
    # this would be separate fields.
    phone = models.CharField(max_length=20)  # Setting max_length to 20 to allow for international numbers.
    email = models.CharField(max_length=50, unique=True)  # unique=True will force validation on creation to confirm
    # that this field is unique among other User models.
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)  # Might consider not using on_delete so
    # that we don't lose the user accounts when we delete the related Organization. (Many to one)
    birthdate = models.DateField()
