import sqlite3
import graphene
from graphene import Mutation
from workshop.schema.types import *


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

        # Delete client from phone database
        conn = sqlite3.connect('movil.db')
        c = conn.cursor()
        c.execute(f"DELETE FROM movil WHERE number = '{item.phone_number}'")
        conn.commit()
        conn.close()
        
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

class DeleteRoadService(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    roadservice = graphene.Field(lambda: RoadServiceType)

    def mutate(self, info, id):
        t = RoadService.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteRoadService(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteRoadService(roadservice=item, ok=True)

class DeleteService(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    service = graphene.Field(lambda: ServiceType)

    def mutate(self, info, id):
        t = Service.objects.filter(pk=id)
        if len(t) == 0:
            return DeleteService(ok=False)
        
        item = t[0]
        t.delete()
        return DeleteService(service=item, ok=True)

class DeletePiece(Mutation):
    class Arguments:
        # The input arguments for this mutation
        id = graphene.String()

    ok = graphene.Boolean()
    piece = graphene.Field(lambda: PieceType)

    def mutate(self, info, id):
        t = Piece.objects.filter(pk=id)
        if len(t) == 0:
            return DeletePiece(ok=False)
        
        item = t[0]
        t.delete()
        return DeletePiece(piece=item, ok=True)
