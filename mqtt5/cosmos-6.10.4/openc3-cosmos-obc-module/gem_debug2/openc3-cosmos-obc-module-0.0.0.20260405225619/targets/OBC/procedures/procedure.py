# Script Runner test script
cmd("OBC EXAMPLE")
wait_check("OBC STATUS BOOL == 'FALSE'", 5)
