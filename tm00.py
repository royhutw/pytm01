#!/usr/bin/env python3

from pytm import (
    TM,
    Actor,
    Boundary,
    Classification,
    Data,
    Dataflow,
    Datastore,
    Lambda,
    Server,
    DatastoreType,
)

tm = TM("Intranet Web - User Login")
tm.isOrdered = True
tm.mergeResponses = True

internet = Boundary("Internet")
internet.levels = [0,1]

dmz = Boundary("DMZ")
dmz.levels = [0,1]

internal_network = Boundary("Internal Network")

user = Actor("User") 
user.inBoundary = internet
user.levels = [0,1]
user.isAdmin = False

httpd = Server("IIS8.5")
httpd.inBoundary = dmz
httpd.levels = [0,1]
httpd.OS = "Windows Server 2012 R2"
httpd.port = 80
httpd.protocol = "HTTP"

dbengine = Server("MSSQL11")
dbengine.inBoundary = internal_network
dbengine.levels = [0,1]
dbengine.OS = "Windows Server 2012 R2"
dbengine.port = 1433
dbengine.protocol = "TCP"

Db = Datastore("IntranetWebDB")
Db.inBoundary = internal_network
Db.levels = [0,1]
Db.isSQL = True
Db.type = DatastoreType.SQL
Db.storesPII = True
Db.storesLogData = True
Db.storesSensitiveData = True

token_user_identity = Data("Token verifying user identity")
token_user_identity.classification = Classification.SECRET
token_user_identity.isPII = False
token_user_identity.isStored = False
token_user_identity.isCredentials = True



user_to_httpd = Dataflow(user, httpd, "Send login credentials")
user_to_httpd.levels = [0,1]
httpd_to_dbengine = Dataflow(httpd, dbengine, "Send hashed password to DB")
httpd_to_dbengine.levels = [0,1]
dbengine_to_httpd = Dataflow(dbengine, httpd, "Send token to verify user identity")



if __name__ == "__main__":
    tm.process()

