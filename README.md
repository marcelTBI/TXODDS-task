# TXODDS-task
Producer-consumer html crawler

Producer goes through urls stored in "urls.txt" (created in the beginning of the example to be self-contained), extracts HTML of the links and stores it in the "to_do" Queue. 

Consumer goes through the "to_do" Queue, parses HTML and writes found hyperlinks to file "output.txt".

Producer and consumer run concurrently and independently. 

Used Python ver. 3.x
