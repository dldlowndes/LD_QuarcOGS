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

        # Ensure line 1 starts with a "1" and line 2 a "2"
        assert self.tle_Dict["line1"][0] == "1"
        assert self.tle_Dict["line2"][0] == "2"

        # Wikipedia says ephemeris type is always 0 so let's test that.
        assert self.ephemeris_type == 0

        # Catalog number is in both lines so might as well make sure they match
        assert int(self.tle_Dict["line2"][2:7]) == self.catalog_Number

        self.checksum_1 = self.tle_Dict["line1"][68]
        my_checksum_1 = Calc_Checksum(self.tle_Dict["line1"])
        # Ensure the checksum value in the line matches the calculated checksum
        assert int(self.checksum_1) == my_checksum_1

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

    @property
    def name(self):
        return self.tle_Dict["line0"]

    @property
    def catalog_Number(self):
        return int(self.tle_Dict["line1"][2:7])

    @property
    def classification(self):
        return self.tle_Dict["line1"][7]

    @property
    def designator(self):
        des = self.tle_Dict["line1"][9:17]
        launch_year = int(des[0:2])
        launch_num = int(des[2:5])
        inter_des = des[5:7].strip()
        return launch_year, launch_num, inter_des

    @property
    def epoch(self):
        self.epoch_str = self.tle_Dict["line1"][18:32]
        # Translate epoch straight into something actually useful!
        epoch_year = datetime.datetime(2000 + int(self.epoch_str[:2]), 1, 1)
        epoch_days = datetime.timedelta(days=float(self.epoch_str[2:]))
        epoch = epoch_year + epoch_days
        return epoch

    @property
    def first_derivative(self):
        return float(self.tle_Dict["line1"][33:43])

    @property
    def second_derivative(self):
        line = self.tle_Dict["line1"][44:52]
        decimal, power = line.split("-")
        value = float("0." + decimal.strip()) * 10**-int(power)
        return value

    @property
    def drag_term(self):
        line = self.tle_Dict["line1"][53:61]
        decimal, power = line.split("-")
        value = float("0." + decimal.strip()) * 10**-int(power)
        return value

    @property
    def ephemeris_type(self):
        return int(self.tle_Dict["line1"][62])

    @property
    def set_number(self):
        return int(self.tle_Dict["line1"][64:68])

    @property
    def inclination(self):
        return float(self.tle_Dict["line2"][8:16])

    @property
    def raan(self):
        return float(self.tle_Dict["line2"][17:25])

    @property
    def eccentricity(self):
        line = self.tle_Dict["line2"][26:33]
        value = float("0."+line.strip())
        return value

    @property
    def perigree(self):
        return float(self.tle_Dict["line2"][34:42])

    @property
    def mean_anomaly(self):
        return float(self.tle_Dict["line2"][43:51])

    @property
    def mean_motion(self):
        return float(self.tle_Dict["line2"][52:63])

    @property
    def revolution_number(self):
        return int(self.tle_Dict["line2"][63:68])
