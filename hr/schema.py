import graphene
from graphene_django import DjangoObjectType

from .models import Messages

# create graph type for view Messages
class MessagesType(DjangoObjectType):
        class Meta:
                model = Messages
                description = 'This is the MessagesType for employees in mysql database'

# Class for graph Query
class Query(graphene.ObjectType):
        class Meta:
                description = 'This is the Query object for messages in mysql database'
        messages   = graphene.List(MessagesType)

        def resolve_messages(self, info, **kwargs):
                return Messages.objects.using('mysql_emp')
