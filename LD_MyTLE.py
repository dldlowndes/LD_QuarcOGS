import datetime

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

        # Might as well split out all the elements in the constructor.
        line1_Split = self.tle_Dict["line1"].split()
        line2_Split = self.tle_Dict["line2"].split()
        self.name = self.tle_Dict["line0"]
        self.line1 = line1_Split[0]
        self.catalog_Number = line1_Split[1][:-1]
        self.classification = line1_Split[1][-1:]
        self.designator = line1_Split[2]
        self.epoch_str = line1_Split[3]
        #Translate epoch straight into something actually useful!
        epoch_year = datetime.datetime(2000 + int(self.epoch_str[:2]), 1, 1)
        epoch_days = datetime.timedelta(days=float(self.epoch_str[2:]))
        self.epoch = epoch_year + epoch_days
        self.first_Derivative = line1_Split[4]
        self.second_Derivative = line1_Split[5]
        self.drag_Term = line1_Split[6]
        self.ephemeris_Type = line1_Split[7]
        self.set_Number = line1_Split[8][:-1]
        self.checksum_1 = line1_Split[8][-1:]

        self.line2 = line2_Split[0]
        #assert line2_Split[1] == self.catalog_Number
        self.inclination = line2_Split[2]
        self.raan = line2_Split[3]
        self.eccentricity = line2_Split[4]
        self.perigree = line2_Split[5]
        self.mean_anomaly = line2_Split[6]
        self.mean_motion = line2_Split[7][:10]
        self.revolution_Number = line2_Split[7][11:-1]
        self.checksum_2 = line2_Split[7][-1:]

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