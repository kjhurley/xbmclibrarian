These tests should cover the main sunny day user stories.


** Test Cases
Check first recording found
    Load First Data
	Is data refreshed 
	Is there a new recording
	Is new recording a TV SHow
	New recording title matches   The Big Bang Theory
	Does new recording have episode title
	Is there a match in tvdb
	New recording season and episode matches   3    13   
    [Tags]   Sunny Day   Identifying Episodes


Check single new recording found
    Load First Data
	Is data refreshed
    Load Second Data 
	Is there a new recording
	Is new recording a TV Show
	New recording title matches   Treasures of Ancient Egypt
	Does new recording have episode title
	Is there a match in tvdb
	New recording season and episode matches   1    2   
    [Tags]   Sunny Day   Identifying Episodes
  
	
Identify recording for new series
    Load First Data
	Is data refreshed
    Load Second Data 
    Load Third Data
	Is new recording a TV Show
	New recording title matches   The Big Bang Theory
	Does new recording have episode title
	Is there a match in tvdb
	New recording season and episode matches   7    8   
    [Tags]   Sunny Day   Identifying Episodes  
    
Narrow the search
    Load First Data
    Select a TVH Recording  23
    Expect number of matches using  2   Ottoman   
    

*** Setting ***
Library     bdd/librarian_tests.py                     
                   

