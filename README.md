#Checkpoint-Scanner

Checkpoint-Scanner utilizes Python code to track magnetic card swipes across various locations during Section Conference.
Each attendee will be carrying a magnetic ID card with them at all times which contains a unique user ID on each card and their name.
Each station during the section conference will have a card reader attached to a Raspberry Pi which will maintain a database of who
has checked into the station and at which times. Each station will be assigned a specific time blocking system which states when and
where the attendees should be at. When an attendee scans his or her badge at the location, the script will cross-check the database
and make sure that the user hasn't already checked in at that point. Other developments may arise to match specific needs as to the
logistics of the campout.

##Features:
- Python
- MySQL
- Raspberry Pi
- Card reader
- Magnetic cards

#Goal:

* Implement the following:
  * Create a malleable node structure which allows for each scanner to manage the data it needs.
    * Develop in an object-oriented manner to ensure that the code base can be reused among each station, only requiring a minor change to fit current needs.
  * Each node needs to:
    1. Wait for user input.
    2. Read in card data when swiped.
    3. Check whether or not that ID has been swiped during the current time block (session).
      * If it has been swiped: deny re-entry, return in error.
      * If it hasn't been swiped: write entry to database, recording ID, and time of entry (epoch time).
  * Lunch lines will have different nodes:
    1. If the user has checked in again during the first session, they will be denied entry.
    2. After the second session, users will be allowed to check in again.
    3. Upon error, the code will issue a warning statement on the accompanying monitor which will display accesibility for the user.
