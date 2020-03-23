import sqlite3
import graphene
from graphene import Mutation
from workshop.schema.types import *
from datetime import datetime as dt
from django.contrib.auth.hashers import make_password


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

    def mutate(self, info, client_id, phone_number, hardware_id, datetime=None, user_id=None, entry_conditions=None):
        entry = Entry()
        entry.client = Client.objects.get(pk=client_id)
        entry.phone_number = phone_number
        if entry_conditions:
            entry.entry_conditions = entry_conditions
        entry.hardware = Hardware.objects.get(pk=hardware_id)
        if datetime:
            entry.datetime = dt.strptime(datetime, "%Y-%m-%d %H:%M:%S")
        if user_id:
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

    def mutate(self, info, client_id, address, phone_number, hardware_id, user_id=None, customer_observation=None, appointment_datetime=None, fixed_appointment_datetime=None):
        roadentry = RoadEntry()
        roadentry.client = Client.objects.get(pk=client_id)
        if user_id:
            roadentry.user = User.objects.get(pk=user_id)
        roadentry.address = address
        roadentry.phone_number = phone_number
        roadentry.hardware = Hardware.objects.get(pk=hardware_id)
        if customer_observation:
            roadentry.customer_observation = customer_observation
        if appointment_datetime:
            roadentry.appointment_datetime = dt.strptime(appointment_datetime, "%Y-%m-%d %H:%M:%S")
        if fixed_appointment_datetime:
            roadentry.fixed_appointment_datetime = dt.strptime(fixed_appointment_datetime, "%Y-%m-%d %H:%M:%S")

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

    def mutate(self, info, name, phone_number, address, municipality, source_id, comment=None):
        client = Client()
        client.name = name
        client.phone_number = phone_number
        client.address = address
        client.address = address 
        client.municipality = municipality
        client.source = Source.objects.get(pk=source_id)
        if None:
            client.comment = comment

        client.save()

        # Save client's contact info to phone database
        conn = sqlite3.connect('movil.db')
        c = conn.cursor()
        c.execute(f"INSERT INTO movil VALUES ('{phone_number}','{name}','', '{address}', '')")
        conn.commit()
        conn.close()

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

    def mutate(self, info, brand, model, type, serial_number=None):
        hardware = Hardware()
        hardware.brand = brand
        hardware.model = model
        hardware.type = type
        if serial_number:
            hardware.serial_number = serial_number 

        hardware.save()
        return CreateHardware(hardware=hardware, ok=True)

class CreateOtherPiece(Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String()
        price = graphene.Float()
        count = graphene.Int()

    ok = graphene.Boolean()
    other_piece = graphene.Field(lambda: OtherPieceType)

    def mutate(self, info, name, price, count):
        other_piece = OtherPiece()
        other_piece.name = name
        other_piece.price = price
        other_piece.count = count

        other_piece.save()
        return CreateOtherPiece(other_piece=other_piece, ok=True)

class CreateFix(Mutation):
    class Arguments:
        # The input arguments for this mutation
        base_price = graphene.Float()
        pieces = graphene.List(graphene.String)
        other_pieces = graphene.List(graphene.String)

    ok = graphene.Boolean()
    fix = graphene.Field(lambda: FixType)

    def mutate(self, info, base_price, pieces=None, other_pieces=None):
        fix = Fix()
        fix.base_price = base_price
        fix.save()

        if pieces:
            fix.pieces.clear()
            ps = [PieceRequest.objects.get(pk=i) for i in pieces]
            for piece in ps:
               fix.pieces.add(piece)

        if other_pieces:
            fix.other_pieces.clear()
            ps = [OtherPieceRequest.objects.get(pk=i) for i in other_pieces]
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

    def mutate(self, info, user_id, state, hardware_id, fix_id, staff_annotations=None, datetime=None):
        subroadservice = SubRoadService()
        subroadservice.user = User.objects.get(pk=user_id)
        subroadservice.state = state
        subroadservice.hardware = Hardware.objects.get(pk=hardware_id)
        if staff_annotations:
            subroadservice.staff_annotations = staff_annotations
        subroadservice.fix = Fix.objects.get(pk=fix_id)
        if datetime:
            subroadservice.datetime = dt.strptime(datetime, "%Y-%m-%d %H:%M:%S")

        subroadservice.save()
        return CreateSubRoadService(subroadservice=subroadservice, ok=True)

class CreateRoadService(Mutation):
    class Arguments:
        # The input arguments for this mutation
        user_id = graphene.String()
        state = graphene.String()
        staff_annotations = graphene.String()
        fix_id = graphene.String()
        datetime = graphene.String()
        otherservices_ids = graphene.List(graphene.String)
        entry_id = graphene.String()

    ok = graphene.Boolean()
    roadservice = graphene.Field(lambda: RoadServiceType)

    def mutate(self, info, user_id=None, state=None, otherservices_ids=None, fix_id=None, staff_annotations=None, datetime=None):
        roadservice = RoadService()
        roadservice.entry = Entry.objects.get(pk=entry_id)
        if user_id:
            roadservice.user = User.objects.get(pk=user_id)
        if state:
            roadservice.state = state
        if staff_annotations:
            roadservice.staff_annotations = staff_annotations
        if fix_id:
            roadservice.fix = Fix.objects.get(pk=fix_id)
        if datetime:
            roadservice.datetime = dt.strptime(datetime, "%Y-%m-%d %H:%M:%S")
        if otherservices_ids:
            ps = [SubRoadService.objects.get(pk=id) for id in otherservices_ids]
            for piece in ps:
               roadservice.others_services.add(piece)

        roadservice.save()
        return CreateRoadService(roadservice=roadservice, ok=True)

class CreateService(Mutation):
    class Arguments:
        # The input arguments for this mutation
        user_id = graphene.String()
        state = graphene.String()
        staff_annotations = graphene.String()
        fix_id = graphene.String()
        datetime = graphene.String()
        otherservices_ids = graphene.List(graphene.String)
        entry_id = graphene.String()

    ok = graphene.Boolean()
    service = graphene.Field(lambda: ServiceType)

    def mutate(self, info, entry_id, user_id=None, state=None, otherservices_ids=None, fix_id=None, staff_annotations=None, datetime=None):
        service = Service()
        service.entry = Entry.objects.get(pk=entry_id)
        if user_id:
            service.user = User.objects.get(pk=user_id)
        if state:
            service.state = state
        if staff_annotations:
            service.staff_annotations = staff_annotations
        if fix_id:
            service.fix = Fix.objects.get(pk=fix_id)
        if datetime:
            service.datetime = dt.strptime(datetime, "%Y-%m-%d %H:%M:%S")
        if otherservices_ids:
            l = [SubService.objects.get(pk=id) for id in otherservices_ids]
            for serv in l:
               service.others_services.add(serv)

        service.save()
        return CreateService(service=service, ok=True)

class CreatePiece(Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String()
        model = graphene.String()
        price = graphene.Float()
        count = graphene.Int()
        min_count = graphene.Int()

    ok = graphene.Boolean()
    piece = graphene.Field(lambda: PieceType)

    def mutate(self, info, price, count, name, model, min_count=None):
        Piece = Piece()
        Piece.name = name
        Piece.model = model
        Piece.count = count
        Piece.price = price
        if min_count:
            Piece.min_count = min_count

        Piece.save()
        return CreatePiece(piece=piece, ok=True)