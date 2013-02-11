#Scanner

Scanner is a python script that is designed to run on a Raspberry Pi station during
Order of the Arrow events held at Seminole Lodge 85. During the event each attendee
will have a barcode ID on their person which will be scanned at these stations for
checking in and checking out. Specialized stations will use a fork of this code base
that will verify the user doesn't check in twice during a specified period (esp. for
verifying lunch line fluidity).

##Features:
- Python
- MySQL interface
- Raspberry Pi
- Barcode scanner

##To-do:
- Create import/export functions for managing barcode scans during check-in/check-out
- Attempt to clean up ncurses boiler-plate
- Implement separate mysql functions for individual tasks (verify nobody has checked in twice in a session, etc)
- Clean up code by using global variables, rearranging function defintions, etc.
