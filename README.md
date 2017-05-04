# graphene-mongoengine
## Supporting mongonengine connection for graphene

Inspired in graphene_django, we can use this package to manage information stored in MongoDB. 

For doing this, we will use Mongoengine package. It's quite simple:

`

    from graphene_mongoengine import MongoEngineObjectType
    
    class MyExampleNode(MongoEngineObjectType):
        class Meta:
            document = MyExampleModel
`