import graphene
from graphene import Mutation, ObjectType
from workshop.constants.models import *
from workshop.schema.types import *
from workshop.schema.m_create import *
from workshop.schema.m_delete import *
from workshop.schema.m_update import *


#--------------------------  WORKSHOP MUTATIONS -----------------------------

class ServiceNextState(Mutation):
    class Arguments:
        # The input arguments for this mutation
        service_id = graphene.String()
        state = graphene.String()

    ok = graphene.Boolean()
    service = graphene.Field(lambda: ServiceType)

    def mutate(self, info, service_id, state):
        service = Service.objects.get(pk=service_id)
        service.state = STATE_CHOICES_WORKSHOP[state][0]
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
        roadservice.state = STATE_CHOICES_ROAD[state][0]
        roadservice.save()
        return ServiceNextState(roadservice=roadservice, ok=True)

#------------------------------------------------------------------------------

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
    create_roadservice = CreateRoadService.Field()
    create_service = CreateService.Field()
    
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
    