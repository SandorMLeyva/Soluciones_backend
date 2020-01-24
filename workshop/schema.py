import graphene
from graphene_django import DjangoObjectType
from workshop.models import *


# Types
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

# Query
class Query(object):
    sources = graphene.List(SourceType)
    clients = graphene.List(ClientType)
    hardwares = graphene.List(HardwareType)
    entries = graphene.List(EntryType)
    services = graphene.List(ServiceType)
    pieces = graphene.List(PieceType)
    otherpieces = graphene.List(OtherPieceType)
    fixs = graphene.List(FixType)
    roadentries = graphene.List(RoadEntryType)
    subroadservices = graphene.List(SubRoadServiceType)
    roadservices = graphene.List(RoadServiceType)
    logs = graphene.List(LogType)

    def resolve_sources(self, info, **kwargs):
        return Source.objects.all()
    def resolve_clients(self, info, **kwargs):
        return Client.objects.all()
    def resolve_hardwares(self, info, **kwargs):
        return Hardware.objects.all()
    def resolve_entries(self, info, **kwargs):
        return Entry.objects.all()
    def resolve_services(self, info, **kwargs):
        return Service.objects.all()
    def resolve_pieces(self, info, **kwargs):
        return Piece.objects.all()
    def resolve_otherpieces(self, info, **kwargs):
        return OtherPiece.objects.all()
    def resolve_fixs(self, info, **kwargs):
        return Fix.objects.all()
    def resolve_roadentries(self, info, **kwargs):
        return RoadEntry.objects.all()
    def resolve_subroadservices(self, info, **kwargs):
        return SubRoadService.objects.all()
    def resolve_roadservices(self, info, **kwargs):
        return RoadService.objects.all()
    def resolve_logs(self, info, **kwargs):
        return Log.objects.all()