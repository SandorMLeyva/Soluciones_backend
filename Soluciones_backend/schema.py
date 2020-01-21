import graphene
import workshop.schema

class Query(workshop.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)