import graphene
from graphene import Mutation, ObjectType
from graphene_django import DjangoObjectType
from workshop.models import *
from workshop.src.stats_queries import *
from django.contrib.auth.hashers import make_password


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


#---------------------  MUTATIONS -----------------------------------

### WORKSHOP
class ServiceNextState(Mutation):
    class Arguments:
        # The input arguments for this mutation
        service_id = graphene.String()
        state = graphene.String()

    ok = graphene.Boolean()
    service = graphene.Field(lambda: ServiceType)

    def mutate(self, info, service_id, state):
        service = Service.objects.get(pk=service_id)
        service.state = state
        service.save()
        return ServiceNextState(service=service, ok=True)

class RoadServiceNextState(Mutation):
    class Arguments:
        # The input arguments for this mutation
        roadservice_id = graphene.String()
        state = graphene.String()

    ok = graphene.Boolean()
    roadservice = graphene.Field(lambda: ServiceType)

    def mutate(self, info, roadservice_id, state):
        roadservice = RoadService.objects.get(pk=roadservice_id)
        roadservice.state = state
        roadservice.save()
        return ServiceNextState(roadservice=roadservice, ok=True)


### CREATE
class CreateUser(Mutation):
    class Arguments:
        # The input arguments for this mutation
        password = graphene.String()
        # last_login = graphene.String()
        # is_superuser = graphene.String()
        username = graphene.String()
        first_name = graphene.String()
        email = graphene.String()
        # is_staff = graphene.String()
        # is_active = graphene.String()
        # date_joined = graphene.String()
        last_name = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserType)

    def mutate(self, info, password, username, first_name, email, last_name):
        user = User()
        user.password = make_password(password)
        user.is_superuser = 1
        user.username = username
        user.first_name = first_name
        user.email = email
        user.is_staff = 1
        user.is_staff = 1
        user.date_joined = str(datetime.datetime.now())
        user.last_name = last_name

        user.save()
        return CreateUser(user=user, ok=True)

class CreateEntry(Mutation):
    class Arguments:
        # The input arguments for this mutation
        client_id = graphene.String()
        phone_number = graphene.String()
        entry_conditions = graphene.String()
        hardware_id = graphene.String()
        datetime = graphene.String()
        user_id = graphene.String()

    ok = graphene.Boolean()
    entry = graphene.Field(lambda: EntryType)

    # def mutate(self, info, client_id, phone_number, entry_conditions, hardware_id, datetime, user_id):
    def mutate(self, info, client_id, phone_number, entry_conditions, hardware_id,  user_id):
        entry = Entry()
        entry.client = Client.objects.get(pk=client_id)
        entry.phone_number = phone_number
        entry.entry_conditions = entry_conditions
        entry.hardware = Hardware.objects.get(pk=hardware_id)
        # entry.datetime = datetime
        entry.user = User.objects.get(pk=user_id)

        entry.save()
        return CreateEntry(entry=entry, ok=True)

class CreateRoadEntry(Mutation):
    class Arguments:
        # The input arguments for this mutation
        client_id = graphene.String()
        user_id = graphene.String()
        address = graphene.String()
        phone_number = graphene.String()
        hardware_id = graphene.String()
        customer_observation = graphene.String()
        appointment_datetime = graphene.String()
        fixed_appointment_datetime = graphene.String()

    ok = graphene.Boolean()
    roadentry = graphene.Field(lambda: RoadEntryType)

    def mutate(self, info, client_id, user_id, address, phone_number, hardware_id, customer_observation, appointment_datetime, fixed_appointment_datetime):
        roadentry = RoadEntry()
        roadentry.client = Client.objects.get(pk=client_id)
        roadentry.user = User.objects.get(pk=user_id)
        roadentry.address = address
        roadentry.phone_number = phone_number
        roadentry.hardware = Hardware.objects.get(pk=hardware_id)
        roadentry.customer_observation = customer_observation
        roadentry.appointment_datetime = appointment_datetime
        roadentry.fixed_appointment_datetime = fixed_appointment_datetime

        roadentry.save()
        return CreateRoadEntry(roadentry=roadentry, ok=True)

class CreateClient(Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String()
        phone_number = graphene.String()
        address = graphene.String()
        municipality = graphene.String()
        source_id = graphene.String()
        comment = graphene.String()

    ok = graphene.Boolean()
    client = graphene.Field(lambda: ClientType)

    def mutate(self, info, name, phone_number, address, municipality, source_id, comment):
        client = Client()
        client.name = name
        client.phone_number = phone_number
        client.address = address
        client.address = address 
        client.municipality = municipality
        client.source = Source.objects.get(pk=source_id)
        client.comment = comment

        client.save()
        return CreateClient(client=client, ok=True)

class CreateHardware(Mutation):
    class Arguments:
        # The input arguments for this mutation
        brand = graphene.String()
        model = graphene.String()
        type = graphene.String()
        serial_number = graphene.String()

    ok = graphene.Boolean()
    hardware = graphene.Field(lambda: HardwareType)

    def mutate(self, info, brand, model, type, serial_number):
        hardware = Hardware()
        hardware.brand = brand
        hardware.model = model
        hardware.type = type
        hardware.serial_number = serial_number 

        hardware.save()
        return CreateHardware(hardware=hardware, ok=True)

class CreateOtherPiece(Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String()
        price = graphene.Float()

    ok = graphene.Boolean()
    other_piece = graphene.Field(lambda: OtherPieceType)

    def mutate(self, info, name, price):
        other_piece = OtherPiece()
        other_piece.name = name
        other_piece.price = price

        other_piece.save()
        return CreateOtherPiece(other_piece=other_piece, ok=True)

class CreateFix(Mutation):
    class Arguments:
        # The input arguments for this mutation
        base_price = graphene.Float()
        pieces = graphene.List(graphene.Int)
        other_pieces = graphene.List(graphene.Int)

    ok = graphene.Boolean()
    fix = graphene.Field(lambda: FixType)

    def mutate(self, info, base_price, pieces, other_pieces):
        fix = Fix()
        fix.base_price = base_price

        if pieces:
            fix.pieces.clear()
            ps = [Piece.objects.get(pk=i) for i in pieces]
            for piece in ps:
               fix.pieces.add(piece)

        if other_pieces:
            fix.other_pieces.clear()
            ps = [OtherPiece.objects.get(pk=i) for i in other_pieces]
            for piece in ps:
               fix.other_pieces.add(piece)

        fix.save()
        return CreateFix(fix=fix, ok=True)

class CreateSubRoadService(Mutation):
    class Arguments:
        # The input arguments for this mutation
        user_id = graphene.String()
        state = graphene.String()
        hardware_id = graphene.String()
        staff_annotations = graphene.String()
        fix_id = graphene.String()
        datetime = graphene.String()

    ok = graphene.Boolean()
    subroadservice = graphene.Field(lambda: SubRoadServiceType)

    def mutate(self, info, user_id, state, hardware_id, staff_annotations, fix_id, datetime):
        subroadservice = SubRoadService()
        subroadservice.user = User.objects.get(pk=user_id)
        subroadservice.state = state
        subroadservice.hardware = Hardware.objects.get(pk=hardware_id)
        subroadservice.staff_annotations = staff_annotations
        subroadservice.fix = Fix.objects.get(pk=fix_id)
        subroadservice.datetime = datetime

        subroadservice.save()
        return CreateSubRoadService(subroadservice=subroadservice, ok=True)

### UPDATE
class UpdateUser(Mutation):
    class Arguments:
        # The input arguments for this mutation
        user_id = graphene.String()
        password = graphene.String()
        last_login = graphene.String()
        is_superuser = graphene.Int()
        username = graphene.String()
        first_name = graphene.String()
        email = graphene.String()
        is_staff = graphene.Int()
        is_active = graphene.Int()
        date_joined = graphene.String()
        last_name = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserType)

    def mutate(self, info, user_id, password, last_login, is_superuser, username, first_name, email, is_staff, is_active, date_joined, last_name):
        user = User.objects.get(pk=user_id)
        user.password = make_password(password)
        user.last_login = last_login
        user.is_superuser = is_superuser
        user.username = username
        user.first_name = first_name
        user.email = email
        user.is_staff = is_staff
        user.is_active = is_active
        user.date_joined = date_joined
        user.last_name = last_name

        user.save()
        return UpdateUser(user=user, ok=True)

class UpdateEntry(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        client_id = graphene.String()
        phone_number = graphene.String()
        entry_conditions = graphene.String()
        hardware_id = graphene.String()
        datetime = graphene.String()
        user_id = graphene.String()

    ok = graphene.Boolean()
    entry = graphene.Field(lambda: EntryType)

    # def mutate(self, info, id, client_id, phone_number, entry_conditions, hardware_id, datetime, user_id):
    def mutate(self, info, id, client_id, phone_number, entry_conditions, hardware_id, user_id):
        entry = Entry.objects.get(pk=id)
        entry.client = Client.objects.get(pk=client_id)
        entry.phone_number = phone_number
        entry.entry_conditions = entry_conditions
        entry.hardware = Hardware.objects.get(pk=hardware_id)
        # entry.datetime = datetime
        entry.user = User.objects.get(pk=user_id)

        entry.save()
        return UpdateEntry(entry=entry, ok=True)

class UpdateRoadEntry(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        client_id = graphene.String()
        user_id = graphene.String()
        address = graphene.String()
        phone_number = graphene.String()
        hardware_id = graphene.String()
        customer_observation = graphene.String()
        appointment_datetime = graphene.String()
        fixed_appointment_datetime = graphene.String()

    ok = graphene.Boolean()
    roadentry = graphene.Field(lambda: RoadEntryType)

    def mutate(self, info, id, client_id, user_id, address, phone_number, hardware_id, customer_observation, appointment_datetime, fixed_appointment_datetime):
        roadentry = RoadEntry.objects.get(pk=id)
        roadentry.client = Client.objects.get(pk=client_id)
        roadentry.user = User.objects.get(pk=user_id)
        roadentry.address = address
        roadentry.phone_number = phone_number
        roadentry.hardware = Hardware.objects.get(pk=hardware_id)
        roadentry.customer_observation = customer_observation
        roadentry.appointment_datetime = appointment_datetime
        roadentry.fixed_appointment_datetime = fixed_appointment_datetime

        roadentry.save()
        return UpdateRoadEntry(roadentry=roadentry, ok=True)

class UpdateClient(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        name = graphene.String()
        phone_number = graphene.String()
        address = graphene.String()
        municipality = graphene.String()
        source_id = graphene.String()
        comment = graphene.String()

    ok = graphene.Boolean()
    client = graphene.Field(lambda: ClientType)

    def mutate(self, info, id, name, phone_number, address, municipality, source_id, comment):
        client = Client.objects.get(pk=id)
        client.name = name
        client.phone_number = phone_number
        client.address = address
        client.address = address 
        client.municipality = municipality
        client.source = Source.objects.get(pk=source_id)
        client.comment = comment

        client.save()
        return UpdateClient(client=client, ok=True)

class UpdateHardware(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        brand = graphene.String()
        model = graphene.String()
        type = graphene.String()
        serial_number = graphene.String()

    ok = graphene.Boolean()
    hardware = graphene.Field(lambda: HardwareType)

    def mutate(self, info, id, brand, model, type, serial_number):
        hardware = Hardware.objects.get(pk=id)
        hardware.brand = brand
        hardware.model = model
        hardware.type = type
        hardware.serial_number = serial_number 

        hardware.save()
        return UpdateHardware(hardware=hardware, ok=True)

class UpdateOtherPiece(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        name = graphene.String()
        price = graphene.Float()

    ok = graphene.Boolean()
    other_piece = graphene.Field(lambda: OtherPieceType)

    def mutate(self, info, id, name, price):
        other_piece = OtherPiece.objects.get(pk=id)
        other_piece.name = name
        other_piece.price = price

        other_piece.save()
        return UpdateOtherPiece(other_piece=other_piece, ok=True)

class UpdateFix(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        base_price = graphene.Float()
        pieces = graphene.List(graphene.Int)
        other_pieces = graphene.List(graphene.Int)

    ok = graphene.Boolean()
    fix = graphene.Field(lambda: FixType)

    def mutate(self, info, id, base_price, pieces, other_pieces):
        fix = Fix.objects.get(pk=id)
        fix.base_price = base_price

        if pieces:
            fix.pieces.clear()
            ps = [Piece.objects.get(pk=i) for i in pieces]
            for piece in ps:
               fix.pieces.add(piece)

        if other_pieces:
            fix.other_pieces.clear()
            ps = [OtherPiece.objects.get(pk=i) for i in other_pieces]
            for piece in ps:
               fix.other_pieces.add(piece)

        fix.save()
        return UpdateFix(fix=fix, ok=True)

class UpdateSubRoadService(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        user_id = graphene.String()
        state = graphene.String()
        hardware_id = graphene.String()
        staff_annotations = graphene.String()
        fix_id = graphene.String()
        datetime = graphene.String()

    ok = graphene.Boolean()
    subroadservice = graphene.Field(lambda: SubRoadServiceType)

    def mutate(self, info, id, user_id, state, hardware_id, staff_annotations, fix_id, datetime):
        subroadservice = SubRoadService.objects.get(pk=id)
        subroadservice.user = User.objects.get(pk=user_id)
        subroadservice.state = state
        subroadservice.hardware = Hardware.objects.get(pk=hardware_id)
        subroadservice.staff_annotations = staff_annotations
        subroadservice.fix = Fix.objects.get(pk=fix_id)
        subroadservice.datetime = datetime

        subroadservice.save()
        return UpdateSubRoadService(subroadservice=subroadservice, ok=True)

### DELETE
class DeleteUser(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    user = graphene.Field(lambda: UserType)

    def mutate(self, info, id):
        t = User.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteUser(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteUser(entry=item, ok=True)

class DeleteEntry(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    entry = graphene.Field(lambda: EntryType)

    def mutate(self, info, id):
        t = Entry.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteEntry(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteEntry(entry=item, ok=True)

class DeleteRoadEntry(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    roadentry = graphene.Field(lambda: RoadEntryType)

    def mutate(self, info, id):
        t = RoadEntry.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteRoadEntry(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteRoadEntry(roadentry=item, ok=True)

class DeleteClient(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    client = graphene.Field(lambda: ClientType)

    def mutate(self, info, id):
        t = Client.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteClient(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteClient(client=item, ok=True)

class DeleteHardware(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    hardware = graphene.Field(lambda: HardwareType)

    def mutate(self, info, id):
        t = Hardware.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteHardware(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteHardware(hardware=item, ok=True)

class DeleteOtherPiece(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    other_piece = graphene.Field(lambda: OtherPieceType)

    def mutate(self, info, id):
        t = OtherPiece.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteOtherPiece(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteOtherPiece(other_piece=item, ok=True)

class DeleteFix(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    fix = graphene.Field(lambda: FixType)

    def mutate(self, info, id):
        t = Fix.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteFix(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteFix(fix=item, ok=True)

class DeleteSubRoadService(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    subroadservice = graphene.Field(lambda: SubRoadServiceType)

    def mutate(self, info, id):
        t = SubRoadService.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteSubRoadService(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteSubRoadService(subroadservice=item, ok=True)



class Mutation(ObjectType):    
    set_nextstate_service = ServiceNextState.Field()
    set_nextstate_roadservice = RoadServiceNextState.Field()

    create_user = CreateUser.Field()
    create_entry = CreateEntry.Field()
    create_roadentry = CreateRoadEntry.Field()
    create_client = CreateClient.Field()
    create_hardware = CreateHardware.Field()
    create_otherpiece = CreateOtherPiece.Field()
    create_fix = CreateFix.Field()
    create_subroadservice = CreateSubRoadService.Field()

    update_user = UpdateUser.Field()
    update_entry = UpdateEntry.Field()
    update_roadentry = UpdateRoadEntry.Field()
    update_client = UpdateClient.Field()
    update_hardware = UpdateHardware.Field()
    update_otherpiece = UpdateOtherPiece.Field()
    update_fix = UpdateFix.Field()
    update_subroadservice = UpdateSubRoadService.Field()
    
    delete_user = DeleteUser.Field()
    delete_entry = DeleteEntry.Field()
    delete_roadentry = DeleteRoadEntry.Field()
    delete_client = DeleteClient.Field()
    delete_hardware = DeleteHardware.Field()
    delete_otherpiece = DeleteOtherPiece.Field()
    delete_fix = DeleteFix.Field()
    delete_subroadservice = DeleteSubRoadService.Field()