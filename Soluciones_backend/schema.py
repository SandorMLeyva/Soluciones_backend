import graphene
from workshop.schema.mutations import Mutation
from workshop.schema.query import Query as WorkshopQuery

class Query(WorkshopQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)