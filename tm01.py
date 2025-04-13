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
internal_network = Boundary("Internal Network")

server_db = Boundary("Server/DatabaseEngine")
server_db.levels = [2]

admin = Actor("Admin", is_admin=True)  
user = Actor("User")  

web_server = Server("Web Server")
web_server.inBoundary = internet
web_server.OS = "Ubuntu"
web_server.controls.isHardened = True
web_server.controls.sanitizesInput = False
web_server.controls.encodesOutput = True
web_server.controls.authorizesSource = False

database = Datastore("Database")
database.OS = "CentOS"
database.controls.isHardened = False
database.inBoundary = server_db
database.type = DatastoreType.SQL
database.inScope = True
database.maxClassification = Classification.RESTRICTED
database.levels = [2]

secretDb = Datastore("Real Identity Database")
secretDb.OS = "CentOS"
secretDb.controls.isHardened = True
secretDb.inBoundary = server_db
secretDb.type = DatastoreType.SQL
# .inScopt default:True "Is the element in scope of the threat model"
secretDb.inScope = True
secretDb.storesPII = True
secretDb.maxClassification = Classification.TOP_SECRET

user_to_web_server = Dataflow(user, web_server, "View Blog Post")
admin_to_web_server = Dataflow(admin, web_server, "Manage Blog Post")
web_server_to_database = Dataflow(web_server, database, "Save or Retrieve Data")  # Server interacts with the database


if __name__ == "__main__":
    tm.process()

