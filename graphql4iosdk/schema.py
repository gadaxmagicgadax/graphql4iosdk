import graphene
import hr.schema

# Query for getting the data from the server.
class Query(hr.schema.Query, graphene.ObjectType):
	pass

# Create schema
schema = graphene.Schema(query=Query)

