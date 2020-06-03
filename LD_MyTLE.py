class My_TLE:
    """
    Container to make accessing elements of a TLE easier.
    """
    def __init__(self, tle):
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


        line1_Split = self.tle_Dict["line1"].split()
        line2_Split = self.tle_Dict["line2"].split()
        self.name = self.tle_Dict["line0"]
        self.line1 = line1_Split[0]
        self.catalog_Number = line1_Split[1][:-1]
        self.classification = line1_Split[1][-1:]
        self.designator = line1_Split[2]
        self.epoch = line1_Split[3]
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
        return self.tle_Dict

    @property
    def List(self):
        return list(self.tle_Dict.values())

    @property
    def String(self):
        return "\n".join(list(self.tle_Dict.values()))

    def __str__(self):
        return self.String

    def __getitem__(self, i):
        return list(self.tle_Dict.values())[i]