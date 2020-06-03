import datetime
import dateutil
import pytz
import tzlocal
import warnings

import astropy
import astropy.coordinates
import astropy.time

import matplotlib.pyplot as plt
import numpy as np

import sgp4.api

import LD_MyTLE
import LD_TLEList

class LD_PassFinder:
    def __init__(self):
        self.here = None

        self.tle_List = None

    def Set_Position(self, lat, long, height):
        """
        Set the latitude, longitude and height above sea level of the OGS
        position
        """

        self.here = astropy.coordinates.EarthLocation(lat=lat,
                                                      lon=long,
                                                      height=height * astropy.units.m)
        return self.here

    def Search_Time_Range(self, t_start, t_stop, t_interval):
        """
        Provide ISO8601 compatible datetime strings for start/stop.
        Provide interval in minutes (can accept float for smaller intervals)
        """

        self.my_tz = tzlocal.get_localzone()
        t_start_local = self.my_tz.localize(dateutil.parser.parse(t_start))
        t_stop_local = self.my_tz.localize(dateutil.parser.parse(t_stop))

        self.t_start = astropy.time.Time(t_start_local)
        self.t_stop = astropy.time.Time(t_stop_local)
        self.t_step = datetime.timedelta(minutes=t_interval)

        self.utc_Time_Series = []
        ti = self.t_start
        while ti <= self.t_stop:
            self.utc_Time_Series.append(ti)
            ti = ti + self.t_step

        self.jd_Range = np.array([x.jd for x in self.utc_Time_Series])

        return self.utc_Time_Series

    def Get_Local_Times(self):
        local_Times = [t.to_datetime(pytz.utc).astimezone(self.my_tz) for t in self.utc_Time_Series]
        return local_Times

    def Load_TLE_Data(self, tle_List=None):
        """
        Provide a string for this to load a text file of TLEs (likely from
        Celestrak.
        Or provide a LD_TLEList object directly.
        """
        if isinstance(tle_List, str):
            self.tle_List = LD_TLEList.LD_TLE_List(tle_List, False)
        elif isinstance(tle_List, LD_TLEList.LD_TLE_List):
            self.tle_List = tle_List
        else:
            warnings.warn("tle_List provided was neither a string, nor a LD_TLEList object. Nothing happened")

        return self.tle_List

    def Calculate_Passes(self, satellites=None):
        """
        Pass either a single LD_MyTLE object, or a list of them.
        Or leave empty to do ALL of the satellites in the TLE List that was
        loaded by Load_TLE_Data.
        """

        # Get the input into the right form for the following
        if isinstance(satellites, LD_MyTLE.LD_MyTLE):
            print(f"One TLE: {satellites.name}")
            sats = [satellites,]
        elif isinstance(satellites, list):
            print(f"List: {[x.name.rstrip() for x in satellites]}")
            sats = satellites
        else:
            sats = list(self.tle_List)

        # Get the cartesian coordinates (and speeds) of each satellite at each
        # point in the time series defined by Set_Time_Range().
        # Then convert to ITRS (which is apparently more standard than TEME)
        itrs_Data = []
        for tle in sats:
            print(tle.name)
            sat = sgp4.api.Satrec.twoline2rv(tle[1], tle[2])
            e, p, v = sat.sgp4_array(self.jd_Range, np.zeros_like(self.jd_Range))

            # SGP4 gives results in some weird coordinate basis (True Equator Mean Equinox frame (TEME))
            # Get values in the right format to convert to something more intelligible and useful.
            teme_p = astropy.coordinates.CartesianRepresentation(p * astropy.units.km, xyz_axis=1)
            teme_v = astropy.coordinates.CartesianDifferential(v * (astropy.units.km / astropy.units.s), xyz_axis=1)

            # Put the coordinates into astropy so it can convert (then convert)
            # International Terrestrial Reference System (ITRS) makes sense.
            teme = astropy.coordinates.TEME(teme_p.with_differentials(teme_v), obstime = self.utc_Time_Series)
            itrs = teme.transform_to(astropy.coordinates.ITRS(obstime=self.utc_Time_Series))

            itrs_Data.append([tle, itrs])

        # Convert satellite coordinates (relative to earth) into alt/az from
        # this position on earth (set by Set_Position).
        observer = astropy.coordinates.AltAz(location=self.here, obstime=self.utc_Time_Series)
        self.altaz_Data = []
        for tle, position in itrs_Data:
            view = position.transform_to(observer)
            self.altaz_Data.append([tle, view.alt, view.az])

        return self.altaz_Data

    def Plot_Passes(self):
        for tle, alt, az in self.altaz_Data:
            plt.plot(alt)
        plt.ylim(0,90)
        plt.show()

if __name__ == "__main__":
    finder = LD_PassFinder()
    finder.Set_Position(51.456671, -2.601768, 71)
    finder.Search_Time_Range(
            "2020-06-02T23:00:00",
            "2020-06-03T02:00:00",
            1
            )
    #finder.Load_TLE_Data("visual.txt")
    finder.Load_TLE_Data("active.txt")

    t = finder.tle_List.Search_And_Return("starlink")
    data = finder.Calculate_Passes(t)
    #finder.Plot_Passes()

#    tle, alt, az = data[0]
#    timeaa = list(zip(finder.Get_Local_Times(), alt))
#    for t, a in timeaa:
#        print(f"{t}, {a.value}")