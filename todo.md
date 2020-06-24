# Easy:
- Tidy up log levels - they're a random mix of DEBUG and INFO now.
- Verify telescope commands before sending
- Verify that PWI_Status parses info from the hardware correctly

# Medium:
- Error handling (telescope mount and otherwise)
- Add option to filter passes by azimuth
- Parse TLE element values into appropriate variables (not strings) (use @property to remove overhead?)
- Go to the moon (and track it?)

# Hard/Boring:
- Show progress of sat finder in the GUI
- Make the plot look nicer
- Convert LST from the telescope mount to real time
- Figure out if the satellite is still illuminated by the sun
	- Find the most visible satellite *now* (or within some short time)
