#Scanner

Scanner is a python script that is designed to run on a Raspberry Pi station during
Order of the Arrow events held at Seminole Lodge 85. During the event each attendee
will have a barcode ID on their person which will be scanned at these stations for
checking in and checking out. Specialized stations will use a fork of this code base
that will verify the user doesnt have to comment out statements
4. Make each database easy to flush out upon merge
5. Checkpoint system:
  * Users cannot check-in twice in specific amount of time
  * Each station will need to have specific users
    * Should each station have a specific db to cross-check ID

* Per location basis:
  * Needs to track user entry date
  * No need for leaving date
