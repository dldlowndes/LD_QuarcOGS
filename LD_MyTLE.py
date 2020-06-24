import datetime

def _To_CS(c):
    """
    Convert the TLE line characters into their corresponding values for
    calculating the checksum. Integers are their value, minus signs are 1, all
    other characters are 0 (spaces, decimal points, letters)
    """
    assert len(c) == 1

    if c.isdigit():
        return int(c)
    if c == "-":
        return 1
    return 0

def Calc_Checksum(line):
    """
    Calculate the checksum of the line by converting all the characters to
    their integer values, summing and taking modulo 10
    """

    checksum = sum(map(_To_CS, line[:-1]))
    return checksum % 10

class LD_MyTLE:
    """
    Container to make accessing elements of a TLE easier.
    """

    def __init__(self, tle):
        """
        Make the TLE. Try to accept a range of different input formats.
        str: a single string of the whole TLE, with \n to denote lines.
        list, tuple: Of length 3, with a TLE line string per element.
        dict: With keys "line0", "line1", "line2". Values are the TLE line strings

        If the input is not a dict, it is converted into a dict. This is to
        most seamlessly support the LD_Planewave telescope mount interface
        which likes dicts.
        """

        if isinstance(tle, str):
            tle = tle.split("\n")
        # falls through to this one too!
        if isinstance(tle, (list, tuple)):
            assert len(tle) == 3
            self.tle_Dict = {
                "line0": tle[0],
                "line1": tle[1],
                "line2": tle[2]
                }
        elif isinstance(tle, dict):
            self.tle_Dict = tle

        # Check the TLE lines are well formed. In this case by ensuring that
        # the column numbers that are guaranteed to be blank are in fact blank.
        blanks_Line1 = [1, 8, 17, 32, 43, 52, 61, 63]
        blanks_Line2 = [1, 7, 16, 25, 33, 42, 51]
        for b in blanks_Line1:
            assert self.tle_Dict["line1"][b] == " "
        for b in blanks_Line2:
            assert self.tle_Dict["line2"][b] == " "

        self.name = self.tle_Dict["line0"]

        self.line1 = self.tle_Dict["line1"][0]
        self.catalog_Number = self.tle_Dict["line1"][2:7]
        self.classification = self.tle_Dict["line1"][7]
        self.designator = self.tle_Dict["line1"][9:17]
        self.epoch_str = self.tle_Dict["line1"][18:32]
        # Translate epoch straight into something actually useful!
        epoch_year = datetime.datetime(2000 + int(self.epoch_str[:2]), 1, 1)
        epoch_days = datetime.timedelta(days=float(self.epoch_str[2:]))
        self.epoch = epoch_year + epoch_days
        self.first_Derivative = self.tle_Dict["line1"][33:43]
        self.second_Derivative = self.tle_Dict["line1"][44:52]
        self.drag_Term = self.tle_Dict["line1"][53:61]
        self.ephemeris_Type = self.tle_Dict["line1"][62]
        self.set_Number = self.tle_Dict["line1"][64:68]
        self.checksum_1 = self.tle_Dict["line1"][68]
        my_checksum_1 = Calc_Checksum(self.tle_Dict["line1"])
        # Ensure the checksum value in the line matches the calculated checksum
        assert int(self.checksum_1) == my_checksum_1

        self.line2 = self.tle_Dict["line2"][0]
        # Catalog number is in both lines so might as well make sure they match
        assert self.tle_Dict["line2"][2:7] == self.catalog_Number
        self.inclination = self.tle_Dict["line2"][8:16]
        self.raan = self.tle_Dict["line2"][17:25]
        self.eccentricity = self.tle_Dict["line2"][26:33]
        self.perigree = self.tle_Dict["line2"][34:42]
        self.mean_anomaly = self.tle_Dict["line2"][43:51]
        self.mean_motion = self.tle_Dict["line2"][52:63]
        self.revolution_Number = self.tle_Dict["line2"][63:68]
        self.checksum_2 = self.tle_Dict["line2"][68]
        my_checksum_2 = Calc_Checksum(self.tle_Dict["line2"])
        # Ensure the checksum value in the line matches the calculated checksum
        assert int(self.checksum_2) == my_checksum_2

    @property
    def Dict(self):
        """
        Returns the TLE elements as a dictionary.
        """
        return self.tle_Dict

    @property
    def List(self):
        """
        Returns the TLE elements as a list.
        """
        return list(self.tle_Dict.values())

    @property
    def String(self):
        """
        Returns the TLE elements as a string
        """
        return "\n".join(list(self.tle_Dict.values()))

    def __str__(self):
        """
        Allows TLE objects to be printed and show some meaningful information.
        """
        return self.String

    def __getitem__(self, i):
        """
        Allows direct access to the TLE lines.
        """
        return list(self.tle_Dict.values())[i]
