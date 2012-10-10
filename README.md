#SCANNER
=======

This repo holds the software that runs on the custom tracking and permission management system that will be adopted by the OA for large events.

Each user is given a LoCo magnetic stripe card which holds their assigned id.

Scans (punches in and out) are stored in a local MySQL database.

#Todo:

1. Fix database/table names
2. Verify validity of cards and input with hash tables
3. Add debug flag so you don't have to comment out statements
4. Make each database easy to flush out upon merge
5. Checkpoint system:
  * Users cannot check-in twice in specific amount of time
  * Each station will need to have specific users
    * Should each station have a specific db to cross-check ID's for attendance?
  * Add a ncurses interface to make life easier for the operator

* Per location basis:
  * Needs to track user entry date
  * No need for leaving date
