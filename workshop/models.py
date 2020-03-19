from django.db import models
from django.contrib.auth.models import User
from .constants.models import *
# Create your models here.


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
    comment = models.TextField(blank=True)

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
    serial_number = models.CharField(max_length=50, blank=True)

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
    entry_conditions = models.TextField(blank=True)
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE) 
    datetime = models.DateTimeField(auto_now_add=True,auto_now=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        """Meta definition for Entry."""

        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'

    def __str__(self):
        """Unicode representation of Entry."""
        return "%s have %s added by %s"%(self.client, self.hardware, self.user)

class Service(models.Model):
    """Model definition for Service."""

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=STATE_CHOICES_WORKSHOP, default= UNASSIGNED_PENDING)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    staff_annotations = models.TextField(blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True)
    fix = models.ForeignKey('Fix', on_delete=models.SET_NULL, blank=True, null=True)
    seal_number = models.CharField(max_length=30, blank=True, null=True)

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


    class Meta:
        """Meta definition for Piece."""

        verbose_name = 'Piece'
        verbose_name_plural = 'Pieces'

    def __str__(self):
        """Unicode representation of Piece."""
        return "%s %s %s"%(self.name, self.model, self.price)

    def count_warn(self):
        """
        Return True if number of pieces is small
        """
        # TODO Cambiar este numero, permitir poner uno dinamico
        return self.min_count < self.min_count if self.min_count else self.count <= 30

class OtherPiece(models.Model):
    """Model definition for OtherPiece."""

    name = models.CharField(max_length=20, blank=False, null=False)
    price = models.FloatField(blank=False, null=False)

    class Meta:
        """Meta definition for OtherPiece."""

        verbose_name = 'OtherPiece'
        verbose_name_plural = 'OthersPieces'

    def __str__(self):
        """Unicode representation of OtherPiece."""
        return "%s -> %s"%(self.name, self.price)

class Fix(models.Model):
    """Model definition for Fix."""

    base_price = models.FloatField()
    pieces = models.ManyToManyField(Piece, blank=True)
    other_pieces = models.ManyToManyField(OtherPiece,blank=True)

    class Meta:
        """Meta definition for Fix."""

        verbose_name = 'Fix'
        verbose_name_plural = 'Fixes'

    def __str__(self):
        """Unicode representation of Fix."""
        return 'Total price = %s'%(self.total_price())

    def pieces_price(self):
        price = self.pieces.all().aggregate(models.Sum('price'))['price__sum']
        return price if price else 0

    def other_pieces_price(self):
        price = self.other_pieces.all().aggregate(models.Sum('price'))['price__sum']         
        return price if price else 0
    
    def total_price(self):
        return self.base_price + self.pieces_price() + self.other_pieces_price()

class RoadEntry(models.Model):
    """Model definition for RoadEntry."""

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=20) 
    hardware = models.ForeignKey(Hardware, on_delete=models.CASCADE) 
    customer_observation = models.TextField(blank=True)
    appointment_datetime = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    fixed_appointment_datetime = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    

    class Meta:
        """Meta definition for RoadEntry."""

        verbose_name = 'RoadEntry'
        verbose_name_plural = 'RoadEntries'

    def __str__(self):
        """Unicode representation of RoadEntry."""
        return "%s has problem with %s added by %s"%(self.client, self.hardware, self.user)
        
class SubRoadService(models.Model):
    """Model definition for SubRoadService."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=STATE_CHOICES_ROAD, default=REQUESTED)
    hardware = models.ForeignKey(Hardware, null=False, blank=False, on_delete=models.CASCADE)
    staff_annotations =  models.TextField(blank= True)
    fix = models.ForeignKey(Fix, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    # entry = models.ForeignKey(RoadEntry, on_delete=models.CASCADE)


    class Meta:
        """Meta definition for SubRoadService."""

        verbose_name = 'SubRoadService'
        verbose_name_plural = 'SubRoadServices'

    def __str__(self):
        """Unicode representation of SubRoadService."""
        return "%s %s"%(self.state, self.hardware)

class RoadService(models.Model):
    """Model definition for RoadService."""

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    state = models.CharField(max_length=10, choices=STATE_CHOICES_ROAD, default=REQUESTED)
    # hardware = models.ForeignKey(Hardware, null=False, blank=False, on_delete=models.CASCADE)
    staff_annotations =  models.TextField(blank= True)
    fix = models.ForeignKey(Fix, null=True, blank=True, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
    others_services = models.ManyToManyField(SubRoadService, blank=True)
    entry = models.ForeignKey(RoadEntry, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for RoadService."""

        verbose_name = 'RoadService'
        verbose_name_plural = 'RoadServices'

    def __str__(self):
        """Unicode representation of RoadService."""
        return "%s %s"%(self.state, self.entry)

class Log(models.Model):
    """Model definition for Log."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    log = models.CharField(max_length=200)
    datetime = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        """Meta definition for Log."""

        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    def __str__(self):
        """Unicode representation of Log."""
        return "%s -> %s"%(self.user, self.log)

