These tests should cover the main sunny day user stories.


** Test Cases
One new recording found
    Prepare Data
	Is data refreshed 
	Is there a new recording
	Is new recording a TV SHow
	New recording title matches   The Big Bang Theory
	Does new recording have episode title
	Is there a match in tvdb
	New recording season and episode matches   1    1   
  
    [Tags]   Sunny Day   Identifying Episodes

*** Setting ***
Library     bdd/librarian_tests.py                     

*** Setting ***
Suite Setup      Prepare data
Suite Teardown                        

