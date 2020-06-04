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

"""
For calculating the alt/az of satellite(s) from a given location. Intended for
testing the Quarc OGS where we will want to test satellite tracking. Probably
for this load Celestrak's "visual.txt" list of TLEs. 

Usage:
    - Make an instance of this class.
    - Set the position of the OGS (latitude, longitude, height)
    - Set the time range of interest using ISO8601 date time strings.
    - Pass one/some/no TLEs to Caluclate_Passes(). If none are passed, it 
    calculates for ALL the satellites in its internal list (this can be a lot!)
    - Use the alt/az vs time data sets for each TLE to choose which to track

TODO: Filter out passes which don't come over the horizon
TODO: Nicer plotting
TODO: General QoL improvements
TODO: GUI?
TODO: Logging!
TODO: Figure out if the satellite is in sun (more visible?)
"""

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
        Provide ISO8601 compatible date&time strings for start/stop.
        (or python datetime objects)
        Provide interval in minutes (can accept float for smaller intervals)
        
        The datetime strings should be in whatever the time zone of the
        computer running this. They are converted internally to UTC from the
        local time zone for the algorithms.
        """ 

        # Interpret the time stamp input and convert into UTC astropy Time objects
        self.t_start = self._Timestamp_Convert(t_start)
        self.t_stop = self._Timestamp_Convert(t_stop)
        self.t_step = datetime.timedelta(minutes=t_interval)

        # Make all the time stamps that we want data for.
        # I'm sure there's a more elegant way of doing this but it works.
        self.utc_Time_Series = []
        ti = self.t_start
        while ti <= self.t_stop:
            self.utc_Time_Series.append(ti)
            ti = ti + self.t_step

        # sgp4 takes time stamps as julian date (because of course) and also as
        # numpy arrays so do the relevant conversions.
        self.jd_Range = np.array([x.jd for x in self.utc_Time_Series])


        # astropy still wants the time stamps in utc_Time_Series, which map to
        # the ones in jd_Range. But should they actually both be in one (slicable?)
        # container to ensure they are definitely referring to the same times?

        return self.utc_Time_Series

    def _Timestamp_Convert(self, stamp):
        # Seems sensible that the user inputs the datetime in their local time
        # so step 1 of interpreting is getting said time zone.
        self.my_tz = tzlocal.get_localzone()
        
        # Figure out if a ISO8601 string or datetime object were supplied.
        if isinstance(stamp, str):
            stamp_local = self.my_tz.localize(dateutil.parser.parse(stamp))
        elif isinstance(stamp, datetime.datetime):
            stamp_local = self.my_tz.localize(stamp)
        else:
            raise TypeError
            
        # And make into an astropy time object (in UTC)
        return astropy.time.Time(stamp_local)

    def Get_Local_Times(self):
        """
        Return the time range set previously converted back into the local
        time zone.
        """
        
        # Sorry, this is kind of horrible.
        # Converts each astropy time object into a utc datetime object, then
        # converts into the local time zone.
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
    
    def Search_TLE_Data(self, search_String):
        """
        Search for the search_String in the names of all of the satellites in
        the TLE list loaded by Load_TLE_Data. Returns a list if there is more
        than one.
        """
        result = self.tle_List.Search_And_Return(search_String)
        return result

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
        self.altaz_Data = []
        self.errors = []
        observer = astropy.coordinates.AltAz(location=self.here,
                                             obstime=self.utc_Time_Series)
        # Alledgedly sgp4 can take multiple satellites at once but it's plenty
        # fast enough just utilizing the fact that it can return data for
        # multiple time stamps at once.
        for tle in sats:
            print(tle.name)
            sat = sgp4.api.Satrec.twoline2rv(tle[1], tle[2])
            e, p, v = sat.sgp4_array(self.jd_Range, np.zeros_like(self.jd_Range))
            if isinstance(e, int):
                if e !=0:
                    warnings.warn(f"Error with {tle.name}. Skipping")
                    self.errors.append([tle.name, e])
                    continue
            elif isinstance(e, np.ndarray):
                if sum(e) != 0:
                    warnings.warn(f"Error with {tle.name}. Skipping")
                    self.errors.append([tle.name, e])
                    continue

            # SGP4 gives results in some weird coordinate basis (True Equator 
            # Mean Equinox frame (TEME)). Get values in the right format to
            # convert to something more intelligible and useful.
            teme_p = astropy.coordinates.CartesianRepresentation(p * astropy.units.km, xyz_axis=1)
            teme_v = astropy.coordinates.CartesianDifferential(v * (astropy.units.km / astropy.units.s), xyz_axis=1)

            # Put the coordinates into astropy, which can convert between bases
            # using International Terrestrial Reference System (ITRS) coordinates.
            teme = astropy.coordinates.TEME(teme_p.with_differentials(teme_v), obstime = self.utc_Time_Series)
            itrs = teme.transform_to(astropy.coordinates.ITRS(obstime=self.utc_Time_Series))

            # Convert satellite coordinates (relative to earth) into alt/az 
            # from this position on earth (set by Set_Position).
            view = itrs.transform_to(observer)
            self.altaz_Data.append([tle, view.alt, view.az])

        if len(self.errors) > 0:
            print(f"Some errors, see {self.errors}")

        return self.altaz_Data

    def Plot_Passes(self):
        """
        Basic plotting for now. Beware if Calculate_Passes gets given too many
        satellites this will look like technicolour vomit at best and at worst
        just crash.
        """
        for tle, alt, az in self.altaz_Data:
            plt.plot(alt)
        plt.ylim(0,90)
        plt.show()

if __name__ == "__main__":
    finder = LD_PassFinder()
    # Set the location of the OGS
    finder.Set_Position(51.456671, -2.601768, 71)
    # Set the time range to search for passes within.
    # (and the resolution in minutes)
    finder.Search_Time_Range(
            "2020-06-02T23:00:00",
            "2020-06-03T02:00:00",
            1
            )
    
    # Load the TLE data file into the finder.
    #finder.Load_TLE_Data("visual.txt")
    finder.Load_TLE_Data("active.txt")

    # Find some values in the TLE list.
    t1 = finder.Search_TLE_Data("zarya") # just the ISS
    t2 = finder.Search_TLE_Data("starlink") # all the starlink satellites (!)
    
    # Calculate the alt/az (degrees) at the time intervals specified for all
    # the satellites passed in. Outputs in the format [<tle_Obj>, <alt>, <az>]
    data = finder.Calculate_Passes(t1)
    
    #finder.Plot_Passes()