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

dmz = Boundary("DMZ")

internal_network = Boundary("Internal Network")

user = Actor("User") 
user.inBoundary = internet

httpd = Server("IIS8.5")
httpd.inBoundary = dmz
httpd.port = 80
httpd.protocol = "HTTP"
httpd.OS = "Windows Server 2012 R2"

dbengine = Server("MSSQL11")
dbengine.inBoundary = internal_network
dbengine.port = 1433
dbengine.protocol = "TCP"
dbengine.OS = "Windows Server 2012 R2"

Db = Datastore("IntranetWebDB")
Db.inBoundary = internal_network
Db.type = DatastoreType.SQL

token_user_identity = Data(
    "Token verifying user identity", classification=Classification.SECRET
)

user_to_httpd = Dataflow(user, httpd, "Send login credentials")
httpd_to_dbengine = Dataflow(httpd, dbengine, "Send hashed password to DB")
dbengine_to_httpd = Dataflow(dbengine, httpd, "Send token to verify user identity")


if __name__ == "__main__":
    tm.process()

