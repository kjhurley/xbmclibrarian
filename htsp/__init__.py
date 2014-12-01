"""

htsmsg - convert hts messages over the wire into python friendly structs
htsp - python api for handling communication with tvheadend (htsp)
htsprefresh - retrieve latest epg dump from htsp (asynchronously)


@startuml
class htsmsg
class HTSPClient {
  send
  recv
  hello
  authenticate
  enableAsyncMetadata
}
class Refresh {
  connect
  read_some_data
  }
@enduml


@startuml
actor System
System->Refresh: create (server, port, user, password)
System->Refresh: connect(server, port)
Refresh->HTSPClient: create
Refresh->HTSPClient: hello
Refresh->HTSPClient: authenticate(user, password)
Refresh->HTSPClient: enableAsyncMetadata("epg")
loop
   System->Refresh: read_some_data
   note over Refresh
      read_some_data is 
      implemented as a generator
   end note
   Refresh->HTSPClient: message = recv
   alt is message initialSyncCompleted?
     note over Refresh: break out of loop
   else
     Refresh -->System: yield message 
   end
end
@enduml
"""