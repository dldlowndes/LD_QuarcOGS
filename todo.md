# Easy:
- Tidy up log levels - they're a random mix of DEBUG and INFO now.
- Verify telescope commands before sending
- Let pass finder accept datetime objects as well as string timestamps
- Verify that PWI_Status parses info from the hardware correctly

# Medium:
- Load multiple TLE files at once
- Error handling (telescope mount and otherwise)
- Add option to filter passes by azimuth
- Assert the TLE checksums are how they should be
- Go to the moon (and track it?)

# Hard/Boring:
- Show progress of sat finder in the GUI
- Make the plot look nicer
- Convert LST from the telescope mount to real time
- Figure out if the satellite is still illuminated by the sun
	- Find the most visible satellite *now* (or within some short time)