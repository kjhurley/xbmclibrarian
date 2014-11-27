"""

@startuml
start
:restore last states;
note right: Use pickle?
:search latest available file info;
note right: look in iplayer log file and get data from htsp
:compare against last know files;
note right: last know files will be those listed in restored object
while (new file info?) is (found one)
  if (kind of info?) then (iplayer)
    :process iplayer file;
  else (htsp)
    :process htsp file;
  endif
  :build episode;
  :build new filename under xbmc;
  if (store using copy?) then (yes)
    :copy file to new filename;
  elseif (store using move?) then (yes)
    :move file to new filename;
    else (store using link)
     :link file to new filename;
  endif
  :record this file in list of know files;
endwhile (none)
:save current state including all known files;
stop
@enduml

Web Sequence Diagram for scenario...



"""