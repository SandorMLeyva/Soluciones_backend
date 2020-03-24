import graphene
from graphene_django import DjangoObjectType
from workshop.models import *

#---------------------  TYPES -----------------------------------
class UserType(DjangoObjectType):
    class Meta:
        model = User

class SourceType(DjangoObjectType):
    class Meta:
        model = Source

class ClientType(DjangoObjectType):
    class Meta:
        model = Client

class HardwareType(DjangoObjectType):
    class Meta:
        model = Hardware

class EntryType(DjangoObjectType):
    class Meta:
        model = Entry

class ServiceType(DjangoObjectType):
    class Meta:
        model = Service

class PieceType(DjangoObjectType):
    class Meta:
        model = Piece

class OtherPieceType(DjangoObjectType):
    class Meta:
        model = OtherPiece

class PieceRequestType(DjangoObjectType):
    class Meta:
        model = PieceRequest

class OtherPieceRequestType(DjangoObjectType):
    class Meta:
        model = OtherPieceRequest

class FixType(DjangoObjectType):
    class Meta:
        model = Fix

class RoadEntryType(DjangoObjectType):
    class Meta:
        model = RoadEntry

class SubRoadServiceType(DjangoObjectType):
    class Meta:
        model = SubRoadService

class RoadServiceType(DjangoObjectType):
    class Meta:
        model = RoadService

class LogType(DjangoObjectType):
    class Meta:
        model = Log

# Queries output types
class SourceCount(graphene.ObjectType):
    source = graphene.String()
    count = graphene.Int()
    
class WorkerEarnings(graphene.ObjectType):
    worker = graphene.String()
    earnings = graphene.Float()

class WorkCompletionStats(graphene.ObjectType):
    completed_services = graphene.Int()
    uncompleted_services = graphene.Int()
    completed_roadservices = graphene.Int()
    uncompleted_roadservices = graphene.Int()

class WorksPerYears(graphene.ObjectType):
    years = graphene.List(graphene.String)
    count = graphene.List(graphene.Int)
    
class WorksPerMonths(graphene.ObjectType):
    months = graphene.List(graphene.String)
    count = graphene.List(graphene.Int)

class WorksDuringWeek(graphene.ObjectType):
    week = graphene.String()
    count = graphene.Int()

class MoneyPerYears(graphene.ObjectType):
    years = graphene.List(graphene.String)
    total = graphene.List(graphene.Int)
    
class MoneyPerMonths(graphene.ObjectType):
    months = graphene.List(graphene.String)
    total = graphene.List(graphene.Int)

class MoneyDuringWeek(graphene.ObjectType):
    week = graphene.String()
    total = graphene.Int()

class ServiceCount(graphene.ObjectType):
    count = graphene.Int()

class KeywordSearch(graphene.ObjectType):
    services = graphene.List(ServiceType)
    roadservices = graphene.List(RoadServiceType)