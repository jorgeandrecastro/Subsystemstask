# Script Runner test script
cmd("COMMS EXAMPLE")
wait_check("COMMS STATUS BOOL == 'FALSE'", 5)
