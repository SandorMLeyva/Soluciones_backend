from django.db import models
from .constants.models import *
#TODO: revisar el delete en cascada
# Create your models here.


# Fijarse que aqui se puede usar el mismo del auth
class User(models.Model):
    """Model definition for User."""

    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        """Meta definition for User."""

        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        """Unicode representation of User."""
        pass


class Source(models.Model):
    """Client's Source."""
    name = models.CharField(max_length=250,blank=False,null=False)

    class Meta:
        """Meta definition for Source."""

        verbose_name = 'Source'
        verbose_name_plural = 'Sources'

    def __str__(self):
        """Unicode representation of Source."""
        return self.name

class Client(models.Model):
    """Model definition for Client."""

    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    municipality = models.CharField(max_length=20)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    comment = models.TextField()

    class Meta:
        """Meta definition for Client."""

        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        """Unicode representation of Client."""
        return self.name

class Hardware(models.Model):
    """Model definition for Hardware."""
    brand = models.CharField(max_length=50, blank=False, null=False)
    model = models.CharField(max_length=50)
    type = models.CharField(max_length=50, blank=False, null=False)
    serial_number = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Hardware."""

        verbose_name = 'Hardware'
        verbose_name_plural = 'Hardwares'

    def __str__(self):
        """Unicode representation of Hardware."""
        return "%s %s %s"%(self.type, self.brand, self.model)

class Entry(models.Model):
    """Model definition for Entry."""

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20) 
    entry_conditions = models.TextField()
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE) 
    datetime = models.DateTimeField(auto_now_add=True,auto_now=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Entry."""

        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    def __str__(self):
        """Unicode representation of Entry."""
        return "%s have %s added by %s"%(self.client, self.hardware, self.user)


class Service(models.Model):
    """Model definition for Service."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=STATE_CHOICES_WORKSHOP, default= UNASSIGNED_PENDING)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    staff_annotations = models.TextField()
    date = models.DateField(auto_now=False, auto_now_add=True)
    fix = models.ForeignKey('Fix', on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Service."""

        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        """Unicode representation of Service."""
        return "%s %s"%(self.state, self.entry)

class Piece(models.Model):
    """Model definition for Piece."""

    name = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    price = models.FloatField(blank=False, null=False)
    count = models.IntegerField(default=0, blank=False, null= False)
    min_count = models.IntegerField(default=0, blank= True, null= True)
    fix = models.ForeignKey('Fix', null=True, blank=True, on_delete=models.CASCADE)


    class Meta:
        """Meta definition for Piece."""

        verbose_name = 'Piece'
        verbose_name_plural = 'Pieces'

    def __str__(self):
        """Unicode representation of Piece."""
        return "%s %s %s"%(self.name, self.model, self.price)

    def count_warn(self):
        """
        Return True if number of pices is small
        """
        # TODO Cambiar este numero, permitir poner uno dinamico
        return self.min_count < self.min_count if self.min_count else self.count <= 30


class OtherPiece(models.Model):
    """Model definition for OtherPiece."""

    name = models.CharField(max_length=20, blank=False, null=False)
    price = models.FileField(blank=False, null=False, default = 0)
    fix = models.ForeignKey('Fix', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for OtherPiece."""

        verbose_name = 'OtherPiece'
        verbose_name_plural = 'OthersPieces'

    def __str__(self):
        """Unicode representation of OtherPiece."""
        return "%s -> %s"%(self.name, self.price)


# TODO: Agregar metodos o formas faciles de resolver todos sus campos (precio final)
class Fix(models.Model):
    """Model definition for Fix."""

    base_price = models.FloatField()

    class Meta:
        """Meta definition for Fix."""

        verbose_name = 'Fix'
        verbose_name_plural = 'Fixes'

    def __str__(self):
        """Unicode representation of Fix."""
        pass


class RoadEntry(models.Model):
    """Model definition for RoadEntry."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=20) 
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE) 
    customer_observation = models.TextField()
    appointment_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)
    fixed_appointment_datetime = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        """Meta definition for RoadEntry."""

        verbose_name = 'RoadEntry'
        verbose_name_plural = 'RoadEntries'

    def __str__(self):
        """Unicode representation of RoadEntry."""
        return "%s has problem with %s added by %s"%(self.client, self.hardware, self.user)
        



class RoadService(models.Model):
    """Model definition for RoadService."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=STATE_CHOICES_ROAD, default=REQUESTED)
    hardware = models.ForeignKey(Hardware, null=False, blank=False, on_delete=models.CASCADE)
    staff_annotations =  models.TextField()
    fix = models.ForeignKey(Fix, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    entry = models.ForeignKey(RoadEntry, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for RoadService."""

        verbose_name = 'RoadService'
        verbose_name_plural = 'RoadServices'

    def __str__(self):
        """Unicode representation of RoadService."""
        return "%s %s"%(self.state, self.entry)

