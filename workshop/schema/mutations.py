import graphene
from graphene import Mutation, ObjectType
from workshop.constants.models import *
from workshop.schema.types import *
from workshop.schema.m_create import *
from workshop.schema.m_delete import *
from workshop.schema.m_update import *


#--------------------------  WORKSHOP MUTATIONS -----------------------------

class ServiceMoveState(Mutation):
    class Arguments:
        # The input arguments for this mutation
        service_id = graphene.String()
        set_previous = graphene.Boolean()

    ok = graphene.Boolean()
    service = graphene.Field(lambda: ServiceType)

    def mutate(self, info, service_id, set_previous=False):
        service = Service.objects.get(pk=service_id)
        new_state = next(ind+1 for ind, x in enumerate(STATE_CHOICES_WORKSHOP) if x[0] == service.state)
        if set_previous:
            new_state = max(0, new_state-2)
        last_state = len(STATE_CHOICES_WORKSHOP)-1
        service.state = STATE_CHOICES_WORKSHOP[min(last_state, new_state)][0]
        
        service.save()
        return ServiceMoveState(service=service, ok=True)

class RoadServiceMoveState(Mutation):
    class Arguments:
        # The input arguments for this mutation
        roadservice_id = graphene.String()
        set_previous = graphene.Boolean()

    ok = graphene.Boolean()
    roadservice = graphene.Field(lambda: RoadServiceType)

    def mutate(self, info, roadservice_id, set_previous=False):
        roadservice = RoadService.objects.get(pk=roadservice_id)
        new_state = next(ind+1 for ind, x in enumerate(STATE_CHOICES_ROAD) if x[0] == roadservice.state)
        last_state = len(STATE_CHOICES_ROAD)-1
        if set_previous:
            new_state = max(0, new_state-2)
        roadservice.state = STATE_CHOICES_ROAD[min(last_state, new_state)][0]
        
        roadservice.save()
        return RoadServiceMoveState(roadservice=roadservice, ok=True)

#------------------------------------------------------------------------------

class Mutation(ObjectType):    
    set_state_service = ServiceMoveState.Field()
    set_state_roadservice = RoadServiceMoveState.Field()

    create_user = CreateUser.Field()
    create_entry = CreateEntry.Field()
    create_roadentry = CreateRoadEntry.Field()
    create_client = CreateClient.Field()
    create_hardware = CreateHardware.Field()
    create_otherpiece = CreateOtherPiece.Field()
    create_fix = CreateFix.Field()
    create_subroadservice = CreateSubRoadService.Field()
    create_roadservice = CreateRoadService.Field()
    create_service = CreateService.Field()
    create_piece = CreatePiece.Field()
    create_piece_request = CreatePieceRequest.Field()
    create_otherpiece_request = CreateOtherPieceRequest.Field()
    
    update_user = UpdateUser.Field()
    update_entry = UpdateEntry.Field()
    update_roadentry = UpdateRoadEntry.Field()
    update_client = UpdateClient.Field()
    update_hardware = UpdateHardware.Field()
    update_otherpiece = UpdateOtherPiece.Field()
    update_fix = UpdateFix.Field()
    update_subroadservice = UpdateSubRoadService.Field()
    update_roadservice = UpdateRoadService.Field()
    update_service = UpdateService.Field()
    update_piece = UpdatePiece.Field() 
    update_piece_request = UpdatePieceRequest.Field()
    update_otherpiece_request = UpdateOtherPieceRequest.Field()
    
    delete_user = DeleteUser.Field()
    delete_entry = DeleteEntry.Field()
    delete_roadentry = DeleteRoadEntry.Field()
    delete_client = DeleteClient.Field()
    delete_hardware = DeleteHardware.Field()
    delete_otherpiece = DeleteOtherPiece.Field()
    delete_fix = DeleteFix.Field()
    delete_subroadservice = DeleteSubRoadService.Field()
    delete_roadservice = DeleteRoadService.Field()
    delete_service = DeleteService.Field()
    delete_piece = DeletePiece.Field() 
    delete_piece_request = DeletePieceRequest.Field()
    delete_otherpiece_request = DeleteOtherPieceRequest.Field()
    