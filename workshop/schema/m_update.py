import sqlite3
import graphene
from graphene import Mutation
from workshop.schema.types import *
from datetime import datetime as dt
from django.contrib.auth.hashers import make_password


### UPDATE
class UpdateUser(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
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

    def mutate(self, info, id, password=None, last_login=None, is_superuser=None, username=None, first_name=None, email=None, is_staff=None, is_active=None, date_joined=None, last_name=None):
        user = User.objects.get(pk=id)
        print(user.__dict__)
        if password:
            user.password = make_password(password)
        if last_login:
            user.last_login = dt.strptime(last_login, "%Y-%m-%d %H:%M:%S")
        if is_superuser:
            user.is_superuser = is_superuser
        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if email:
            user.email = email
        if is_staff:
            user.is_staff = is_staff
        if is_active:
            user.is_active = is_active
        if date_joined:
            user.date_joined = dt.strptime(date_joined, "%Y-%m-%d %H:%M:%S")
        if last_name:
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
        datetime = graphene.types.String()
        user_id = graphene.String()

    ok = graphene.Boolean()
    entry = graphene.Field(lambda: EntryType)

    def mutate(self, info, id, client_id=None, phone_number=None, entry_conditions=None, hardware_id=None, datetime=None, user_id=None):
        entry = Entry.objects.get(pk=id)
        if client_id:
            entry.client = Client.objects.get(pk=client_id)
        if phone_number:
            entry.phone_number = phone_number
        if entry_conditions:
            entry.entry_conditions = entry_conditions
        if hardware_id:
            entry.hardware = Hardware.objects.get(pk=hardware_id)
        if datetime:
            entry.datetime = dt.strptime(datetime, "%Y-%m-%d %H:%M:%S")
        if user_id:
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

    def mutate(self, info, id, client_id=None, user_id=None, address=None, phone_number=None, hardware_id=None, customer_observation=None, appointment_datetime=None, fixed_appointment_datetime=None):
        roadentry = RoadEntry.objects.get(pk=id)
        if client_id:
            roadentry.client = Client.objects.get(pk=client_id)
        if user_id:
            roadentry.user = User.objects.get(pk=user_id)
        if address:
            roadentry.address = address
        if phone_number:
            roadentry.phone_number = phone_number
        if hardware_id:
            roadentry.hardware = Hardware.objects.get(pk=hardware_id)
        if customer_observation:
            roadentry.customer_observation = customer_observation
        if appointment_datetime:
            roadentry.appointment_datetime = dt.strptime(appointment_datetime, "%Y-%m-%d %H:%M:%S")
        if fixed_appointment_datetime:
            roadentry.fixed_appointment_datetime = dt.strptime(fixed_appointment_datetime, "%Y-%m-%d %H:%M:%S")

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

    def mutate(self, info, id, name=None, phone_number=None, address=None, municipality=None, source_id=None, comment=None):
        client = Client.objects.get(pk=id)
        query = "UPDATE movil SET "
        atts = []
        old_num = ""
        if name:
            client.name = name
            atts.append(f"name = '{name}'")
        if phone_number:
            old_num  = client.phone_number
            client.phone_number = phone_number
            atts.append(f"number = '{phone_number}'")
        if address:
            client.address = address
            atts.append(f"address = '{address}'")
        if municipality:
            client.municipality = municipality
        if source_id:
            client.source = Source.objects.get(pk=source_id)
        if comment:
            client.comment = comment

        client.save()

        # Update client in contact database
        conn = sqlite3.connect('movil.db')
        query += ", ".join(atts) + f" WHERE number = {phone_number}"
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()
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

    def mutate(self, info, id, brand=None, model=None, type=None, serial_number=None):
        hardware = Hardware.objects.get(pk=id)
        if brand:
            hardware.brand = brand
        if model:
            hardware.model = model
        if type:
            hardware.type = type
        if serial_number:
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

    def mutate(self, info, id, name=None, price=None):
        other_piece = OtherPiece.objects.get(pk=id)
        if name:
            other_piece.name = name
        if price:
            other_piece.price = price

        other_piece.save()
        return UpdateOtherPiece(other_piece=other_piece, ok=True)

class UpdateFix(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        base_price = graphene.Float()
        pieces = graphene.List(graphene.String)
        other_pieces = graphene.List(graphene.String)

    ok = graphene.Boolean()
    fix = graphene.Field(lambda: FixType)

    def mutate(self, info, id, base_price=None, pieces=None, other_pieces=None):
        fix = Fix.objects.get(pk=id)
        if base_price:
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

    def mutate(self, info, id, user_id=None, state=None, hardware_id=None, staff_annotations=None, fix_id=None, datetime=None):
        subroadservice = SubRoadService.objects.get(pk=id)
        if user_id:
            subroadservice.user = User.objects.get(pk=user_id)
        if state:
            subroadservice.state = state
        if hardware_id:
            subroadservice.hardware = Hardware.objects.get(pk=hardware_id)
        if staff_annotations:
            subroadservice.staff_annotations = staff_annotations
        if fix_id:
            subroadservice.fix = Fix.objects.get(pk=fix_id)
        if datetime:
            subroadservice.datetime = dt.strptime(datetime, "%Y-%m-%d %H:%M:%S")

        subroadservice.save()
        return UpdateSubRoadService(subroadservice=subroadservice, ok=True)

class UpdateRoadService(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        user_id = graphene.String()
        state = graphene.String()
        staff_annotations = graphene.String()
        fix_id = graphene.String()
        datetime = graphene.String()
        otherservices_ids = graphene.List(graphene.String)
        entry_id = graphene.String()

    ok = graphene.Boolean()
    roadservice = graphene.Field(lambda: RoadServiceType)

    def mutate(self, info, id, user_id=None, state=None, otherservices_ids=None, fix_id=None, staff_annotations=None, datetime=None):
        roadservice = RoadService.objects.get(pk=id)
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
        return UpdateRoadService(roadservice=roadservice, ok=True)

class UpdateService(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        user_id = graphene.String()
        state = graphene.String()
        staff_annotations = graphene.String()
        fix_id = graphene.String()
        datetime = graphene.String()
        otherservices_ids = graphene.List(graphene.String)
        entry_id = graphene.String()

    ok = graphene.Boolean()
    service = graphene.Field(lambda: ServiceType)

    def mutate(self, info, id, entry_id=None, user_id=None, state=None, otherservices_ids=None, fix_id=None, staff_annotations=None, datetime=None):
        service = Service.objects.get(pk=id)
        if entry_id:
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
        return UpdateService(service=service, ok=True)

class UpdatePiece(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()
        name = graphene.String()
        model = graphene.String()
        price = graphene.Float()
        count = graphene.Int()
        min_count = graphene.Int()

    ok = graphene.Boolean()
    piece = graphene.Field(lambda: PieceType)

    def mutate(self, info, id, price=None, count=None, name=None, model=None, min_count=None):
        piece = Piece.objects.get(pk=id)
        if name:
            piece.name = name
        if model:
            piece.model = model
        if price:
            piece.price = price
        if count:
            piece.count = count
        if min_count:
            piece.min_count = min_count

        piece.save()
        return UpdatePiece(piece=piece, ok=True)