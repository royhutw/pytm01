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

httpd = Server("IIS8.5 - ASP.NET Web Forms App")
httpd.inBoundary = dmz
httpd.levels = [0,1]
httpd.OS = "Windows Server 2012 R2"
httpd.port = 80
httpd.protocol = "HTTP"

db = Datastore("MSSQL11 - IntranetWebDB")
db.inBoundary = internal_network
db.levels = [0,1]
db.isSQL = True
db.type = DatastoreType.SQL
db.OS = "Windows Server 2012 R2"
db.port = 1433
db.protocol = "TCP"
db.storesPII = True
db.storesLogData = True
db.storesSensitiveData = True

user_to_httpd = Dataflow(user, httpd, "Send login credential")
user_to_httpd.levels = [0,1]
httpd_to_db = Dataflow(httpd, db, "Query user identity")
httpd_to_db.levels = [0,1]
db_to_httpd = Dataflow(db, httpd, "Send user identity")
db_to_httpd.levels = [0,1]
httpd_to_httpd = Dataflow(httpd, httpd, "Keep session in memory")
httpd_to_httpd.levels = [0,1]


if __name__ == "__main__":
    tm.process()

