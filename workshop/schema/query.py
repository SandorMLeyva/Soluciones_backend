import graphene
from workshop.schema.types import  *
from workshop.src.stats_queries import *

#---------------------  QUERIES -----------------------------------
class Query(graphene.ObjectType):
    users = graphene.List(UserType)
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

    user = graphene.Field(UserType, id=graphene.String())
    entry = graphene.Field(EntryType, id=graphene.String())
    roadentry = graphene.Field(RoadEntryType, id=graphene.String())
    client = graphene.Field(ClientType, id=graphene.String())
    hardware = graphene.Field(HardwareType, id=graphene.String())
    otherpiece = graphene.Field(OtherPieceType, id=graphene.String())
    fix = graphene.Field(FixType, id=graphene.String())
    subroadfix = graphene.Field(SubRoadServiceType, id=graphene.String())

    sources_counts = graphene.List(SourceCount)
    workers_earnings = graphene.List(WorkerEarnings)
    work_completion_stats = graphene.Field(WorkCompletionStats)
    works_per_years = graphene.Field(WorksPerYears)
    works_per_months = graphene.Field(WorksPerMonths)
    works_during_week = graphene.Field(WorksDuringWeek, week=graphene.String())
    money_per_years = graphene.Field(MoneyPerYears)
    money_per_months = graphene.Field(MoneyPerMonths)
    money_during_week = graphene.Field(MoneyDuringWeek, week=graphene.String())

    test = graphene.String()
   
    # Query for testing
    def resolve_test(self, info):
        return make_password("1234")

    # Stats Queries
    def resolve_sources_counts(self, info):
        return [ SourceCount(src.name, src.count) for src in sources_counts() ]

    def resolve_workers_earnings(self, info):
            return [ WorkerEarnings(k,v) for k, v in workers_earnings() ]
    
    def resolve_work_completion_stats(self, info):
        stats = work_completion_stats()
        return WorkCompletionStats(
            stats['completed_services'],
            stats['uncompleted_services'],
            stats['completed_roadservices'],
            stats['uncompleted_roadservices'])

    def resolve_works_per_years(self, info):
        years, counts = works_per_years()
        return WorksPerYears(years, counts)
        
    def resolve_works_per_months(self, info):
        months, counts = works_per_months()
        return WorksPerMonths(months, counts)
        
    def resolve_works_during_week(self, info, week):
        week, count = works_during_week(week)
        return WorksDuringWeek(week, count)
        
    def resolve_money_per_years(self, info):
        years, total = money_per_years()
        return MoneyPerYears(years, total)
        
    def resolve_money_per_months(self, info):
        months, total = money_per_months()
        return MoneyPerMonths(months, total)
        
    def resolve_money_during_week(self, info, week):
        wk, total = money_during_week(week)
        return MoneyDuringWeek(wk, total)


    # Read ALL queries
    def resolve_users(self, info, **kwargs):
        return User.objects.all()
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

    # Read ONE Queries
    def resolve_user(self, info, id):
        return User.objects.get(pk=id)
    def resolve_source(self, info, id):
        return Source.objects.get(pk=id)
    def resolve_client(self, info, id):
        return Client.objects.get(pk=id)
    def resolve_hardware(self, info, id):
        return Hardware.objects.get(pk=id)
    def resolve_entry(self, info, id):
        return Entry.objects.get(pk=id)
    def resolve_service(self, info, id):
        return Service.objects.get(pk=id)
    def resolve_piece(self, info, id):
        return Piece.objects.get(pk=id)
    def resolve_otherpiece(self, info, id):
        return OtherPiece.objects.get(pk=id)
    def resolve_fix(self, info, id):
        return Fix.objects.get(pk=id)
    def resolve_roadentry(self, info, id):
        return RoadEntry.objects.get(pk=id)
    def resolve_subroadservice(self, info, id):
        return SubRoadService.objects.get(pk=id)
    def resolve_roadservice(self, info, id):
        return RoadService.objects.get(pk=id)
    def resolve_log(self, info, id):
        return Log.objects.get(pk=id)

