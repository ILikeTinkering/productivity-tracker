# Productivity Tracker

Created this as a project for HackRU Fall 2025.

Minimalist productivity tracker that can detect open applications. If the tracker detects unproductive apps for a specific (adjustable) threshold, it will push a notifcation to the user to encourage them to get back on track.

# Customizability
User can adjust which apps they want to blacklist and the unproductivty timer, though edits must be made within the code (haven't incorporated a way to change anything while in the app window itself)


# Limitations
Unfortunately this only works with open applications. It doesn't work with specifc browser windows as I am unsure how to implement that.
Also, I believe this only works on Windows devices because of the library I used to track active tabs.
