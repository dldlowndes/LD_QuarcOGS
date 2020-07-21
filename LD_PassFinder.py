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
"""

import datetime
import logging
import sys

import astropy
import astropy.coordinates
import astropy.time
import dateutil
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import scipy.signal
import sgp4.api
import tzlocal

import LD_MyTLE
import LD_TLEList

mpl_logger = logging.getLogger("matplotlib")
mpl_logger.setLevel(logging.WARNING)
log = logging.getLogger(__name__)

class LD_PassFinder:
    """
    Calculates passes of satelites.
    """
    def __init__(self):
        log.debug("Set passfinder defaults")
        self.here = None
        self.tle_List = None

        # Knowing timezone seems to be useful a lot of the time so let's put
        # it in the constructor.
        self.my_tz = tzlocal.get_localzone()

    def Set_Position(self, lat, long, height):
        """
        Set the latitude, longitude and height above sea level of the OGS
        position
        """

        log.info(f"Site conditions set to lat={lat}, long={long}, height={height}")
        self.here = astropy.coordinates.EarthLocation(lat=lat,
                                                      lon=long,
                                                      height=height * astropy.units.m)
        return self.here

    def Search_Time_Range(self, t_start, t_stop, t_step):
        """
        Provide ISO8601 compatible date&time strings for start/stop.
        (or python datetime objects)
        Provide interval in minutes (can accept float for smaller intervals)

        The datetime strings should be in whatever the time zone of the
        computer running this. They are converted internally to UTC from the
        local time zone for the algorithms.
        """

        # Interpret the time stamp input and convert into UTC astropy Time objects
        # _Timestamp_Convert() deals with local time zones here
        self.t_start = self._Timestamp_Convert(t_start)
        self.t_stop = self._Timestamp_Convert(t_stop)
        self.t_step = datetime.timedelta(minutes=t_step)

        log.info(f"Set time range start={self.t_start} UTC, stop={self.t_stop} UTC, step={self.t_step}")

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
        # (slicable?) the ones in jd_Range. But should they actually both be in
        # one container to ensure they are definitely referring to the same
        # times?

        return self.utc_Time_Series

    def _Timestamp_Convert(self, stamp):
        """
        Convert timestamps (either ISO strings or datetime objects) into
        localized astropy time stamps.
        """
        log.debug(f"Processing stamp provided as {type(stamp)} to Astropy UTC")

        if not isinstance(stamp, (str, datetime.datetime)):
            raise TypeError

        # If a string was supplied, convert to datetime stamp.
        if isinstance(stamp, str):
            stamp = self.my_tz.localize(dateutil.parser.parse(stamp))

        # Localize the time (if necessary)
        if (stamp.tzinfo is None) or (stamp.tzinfo.utcoffset(stamp) is None):
             stamp = self.my_tz.localize(stamp)

        # And make into an astropy time object (in UTC)
        return astropy.time.Time(stamp)

    def Get_Local_Times(self):
        """
        Return the time range set previously converted back into the local
        time zone.
        """

        # Sorry, this is kind of horrible.
        # Converts each astropy time object into a utc datetime object, then
        # converts into the local time zone.
        local_Times = [t.to_datetime(self.my_tz) for t in self.utc_Time_Series]
        return local_Times

    def Load_TLE_Data(self, tle_List=None):
        """
        Provide a string for this to load a text file of TLEs (likely from
        Celestrak.
        Or provide a LD_TLEList object directly.
        """
        log.info(f"Loading TLE list, list supplied of type {type(tle_List)}")

        if isinstance(tle_List, str):
            self.tle_List = LD_TLEList.LD_TLEList(tle_List)
        elif isinstance(tle_List, LD_TLEList.LD_TLEList):
            self.tle_List = tle_List
        elif isinstance(tle_List, type(None)):
            url = "https://www.celestrak.com/NORAD/elements/active.txt"
            self.tle_List = LD_TLEList.LD_TLEList()
            self.tle_List.Load_TLEs_From_URL(url)
        else:
            log.warning("tle_List provided was neither a string, nor a LD_TLEList object. Nothing happened")

        log.info(f"{len(self.tle_List)} TLEs in the list")

        return self.tle_List

    def Search_TLE_Data(self, search_String):
        """
        Search for the search_String in the names of all of the satellites in
        the TLE list loaded by Load_TLE_Data. Returns a list if there is more
        than one.
        """

        log.info(f"Search TLE list for {search_String}")
        result = self.tle_List.Search_And_Return(search_String)
        if search_String != "":
            log.debug(f"Search result {result}")
        return result

    def Calculate_Passes(self, satellites=None):
        """
        Pass either a single LD_MyTLE object, or a list of them.
        Or leave empty to do ALL of the satellites in the TLE List that was
        loaded by Load_TLE_Data.
        """

        # Get the input into the right form for the following
        if isinstance(satellites, LD_MyTLE.LD_MyTLE):
            #print(f"One TLE: {satellites.name}")
            sats = [satellites,]
        elif isinstance(satellites, list):
            #print(f"List: {[x.name.rstrip() for x in satellites]}")
            sats = satellites
        else:
            sats = list(self.tle_List)

        log.info(f"Calculating passes for {len(sats)} TLEs")

        # Get the cartesian coordinates (and speeds) of each satellite at each
        # point in the time series defined by Set_Time_Range().
        # Then convert to ITRS (which is apparently more standard than TEME)
        self.altaz_Data = []
        self.errors = []
        observer = astropy.coordinates.AltAz(location=self.here,
                                             obstime=self.utc_Time_Series)
        # Alledgedly sgp4 can take multiple satellites at once but it's plenty
        # fast enough just utilizing the fact that it can return data for
        # multiple time stamps at once.
        for tle in sats:
            log.info(f"Calculating pass data for {tle.name}")
            sat = sgp4.api.Satrec.twoline2rv(tle[1], tle[2])
            e, p, v = sat.sgp4_array(self.jd_Range, np.zeros_like(self.jd_Range))
            if isinstance(e, int):
                if e != 0:
                    log.warning(f"Error with {tle.name}. Skipping")
                    self.errors.append([tle.name, e])
                    continue
            elif isinstance(e, np.ndarray):
                if sum(e) != 0:
                    log.warning(f"Error with {tle.name}. Skipping")
                    self.errors.append([tle.name, e])
                    continue

            # SGP4 gives results in some weird coordinate basis (True Equator
            # Mean Equinox frame (TEME)). Get values in the right format to
            # convert to something more intelligible and useful.
            teme_p = astropy.coordinates.CartesianRepresentation(p * astropy.units.km, xyz_axis=1)
            teme_v = astropy.coordinates.CartesianDifferential(v * (astropy.units.km / astropy.units.s), xyz_axis=1)

            # Put the coordinates into astropy, which can convert between bases
            # using International Terrestrial Reference System (ITRS) coordinates.
            teme = astropy.coordinates.TEME(teme_p.with_differentials(teme_v), obstime=self.utc_Time_Series)
            itrs = teme.transform_to(astropy.coordinates.ITRS(obstime=self.utc_Time_Series))

            # Convert satellite coordinates (relative to earth) into alt/az
            # from this position on earth (set by Set_Position).
            view = itrs.transform_to(observer)
            data = pd.DataFrame({
                "time": self.utc_Time_Series,
                "alt": view.alt.data,
                "az": view.az.data
                })
            self.altaz_Data.append([tle, data])

        if len(self.errors) > 0:
            log.warning(f"Some errors, see {self.errors}")

        log.info(f"Finished. {len(self.altaz_Data)} calculated with {len(self.errors)} errors")
        return self.altaz_Data

    def Filter_Passes(self, alt_Filter):
        """
        Filter out all of the data from the passes where the satellite peaks
        below "alt_Filter" degrees altitude.
        """

        log.info(f"Filtering passes with peaks below {alt_Filter} degrees alt")

        # Container for the pass data, each line will comprise the satellite
        # [name, [peak time, peak alt, az@peak], pass data] where pass data is
        # alt/az values for when the satellite is above the horizon.
        self.pass_Data = []
        for sat, data in self.altaz_Data:
            # Find the local maxima in the each satellite's tracks (there may
            # be more than one!)
            alt_peaks = scipy.signal.argrelextrema(data["alt"].values, np.greater)[0]

            # Look at each peak separately.
            for peak in alt_peaks:
                # Get the data at the peak
                time, alt, az = data.iloc[peak]

                # If the peak is high enough to be worth trying to look at.
                if alt > alt_Filter:

                    # First, scan forwards to find when the satellite drops
                    # back below the horizon. This finds the end of the pass.
                    i = peak
                    search_alt = alt
                    while search_alt > 0:
                        i += 1
                        if i >= len(data):
                            break
                        search_alt = data.iloc[i]["alt"]
                    end = (i - 1)

                    # Then scan backwards from the peak to find when the
                    # satellite first came up over the horizon to find the
                    # start of the pass
                    search_alt = alt
                    while search_alt > 0:
                        i -= 1
                        if i < 0:
                            break
                        search_alt = data.iloc[i]["alt"]
                    start = (i + 1)

                    # Extract the portion of the satellite's track data where
                    # it was above the horizon *this time*
                    pass_Isolated = data[start:end]

                    # Add to the rest.
                    # NOTE datetime is converted from UTC back to local TZ here!
                    peak_Info = [time.to_datetime(self.my_tz), alt, az]
                    self.pass_Data.append([sat, peak_Info, pass_Isolated])

        # Sort the passes into chronological order (by peak time), this makes
        # display and plotting easier and prettier.
        self.pass_Data.sort(key=lambda x: x[1][0])
        log.info(f"{len(self.pass_Data)} passes satisfy alt filter")
        return self.pass_Data

    def Get_Pass_List(self):
        """
        Return a neat list of just the TLE, peak time, peak alt, az@peak
        """

        pass_List = []
        for sat in self.pass_Data:
            name = sat[0].name
            time = str(sat[1][0])
            alt = sat[1][1]
            az = sat[1][2]
            pass_List.append({
                "satellite": name.rstrip(),
                "time": time,
                "alt": alt,
                "az": az
                })
        return pd.DataFrame(pass_List)

    def Print_Pass_List(self):
        """
        Print each satellite pass as identified by Filter_Passes(). These are
        already in chronological order so no need to do that.
        """

        data = self.Get_Pass_List()
        # Well, Pandas does have some redeeming features.
        printable = data.to_string()
        print(printable)
        return printable

    def Save_Pass_List(self):
        """
        As with Print_Pass_List(), but dump out to a datestamped csv file.
        """

        # Generate the file name which contains the start and stop times of the
        # scan.
        t_fmt = "%Y-%m-%dT%H-%M-%S"
        filename = "".join(["pass_Data/passes",
                            self.t_start.to_datetime(self.my_tz).strftime(t_fmt),
                            " - ",
                            self.t_stop.to_datetime(self.my_tz).strftime(t_fmt),
                            ".csv"
                            ])

        if not os.path.exists("pass_Data"):
            os.mkdir("pass_Data")
        with open(filename, "w") as f:
            f.write("Name, time, alt, az\n")
            data = self.Get_Pass_List()

            for _, item in data.iterrows():
                f.write(f"{item.satellite}, {item.time}, {item.alt}, {item.az}\n")
        return data.to_string()

    def Plot_All_Passes(self):
        """
        Basic plotting for now. Beware if Calculate_Passes gets given too many
        satellites this will look like technicolour vomit at best and at worst
        just crash.
        """

        log.debug("Plot all passes")

        fig, my_ax = plt.subplots()
        my_ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%H:%M:%S"))
        for sat, data in self.altaz_Data:
            data.plot(x="time", y="alt", ax=my_ax, rot=90)
        plt.show()


    def Plot_Good_Passes(self):
        """
        Plot all passes identified by Filter_Passes() on the same axis.
        """

        log.debug("Plot passes above threshold alt")

        # Make an axis that can be repeatedly plotted onto
        fig, my_ax = plt.subplots()

        for sat, peak_Info, data in self.pass_Data:
            # Make timestamps that matplotlib can understand.
            x_data = [x.plot_date for x in data["time"].values]
            # Altitude is the only particularly interesting feature for these
            # purposes (plotting azimuth as well would be confusing)
            y_data = data["alt"]
            my_ax.plot_date(x_data, y_data, xdate=True,
                            linestyle="-", marker=None)

            label_text = sat.name.rstrip()
            label_pos_x = matplotlib.dates.date2num(peak_Info[0])
            label_pos_y = peak_Info[1]

            my_ax.text(label_pos_x, label_pos_y, label_text)

        my_ax.xaxis_date(self.my_tz)
        fmt = matplotlib.dates.DateFormatter("%Y/%m/%d %H:%M")
        my_ax.xaxis.set_major_formatter(fmt)

        # Get the axes looking nice.
        my_ax.xaxis.set_major_locator(matplotlib.dates.MinuteLocator(interval=15))
        my_ax.grid(True, which="major", axis="both", linestyle="--")

        my_ax.xaxis.set_minor_locator(matplotlib.dates.MinuteLocator(interval=5))
        my_ax.grid(True, which="minor", axis="both", linestyle=":")

        my_ax.xaxis.set_tick_params(rotation=90)

        my_ax.set_ylim(0, 90)
        my_ax.set_xlim(self.t_start.plot_date, self.t_stop.plot_date)

        fig.show()

if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    finder = LD_PassFinder()
    # Set the location of the OGS
    finder.Set_Position(51.456671, -2.601768, 71)
    # Set the time range to search for passes within.
    # (and the resolution in minutes)
    finder.Search_Time_Range(
        "2020-06-11T22:00:00",
        "2020-06-12T06:00:00",
        1
        )

    # Load the TLE data file into the finder.
    finder.Load_TLE_Data("tle_Files/visual.txt")
    #finder.Load_TLE_Data("tle_Files/active.txt") # a very big list!
    #finder.Load_TLE_Data("tle_Files/cubesat.txt")
    #finder.Load_TLE_Data() # Go get Celestrak's "active" list from the internet.

    # Find some values in the TLE list.
    # Find TLE lists on:
    #   - https://www.celestrak.com/NORAD/elements/
    #   - https://www.space-track.org
    # Maybe find candidates on https://in-the-sky.org/satpasses.php
    t1 = finder.Search_TLE_Data("zarya") # just the ISS
    t2 = finder.Search_TLE_Data("starlink") # all the starlink satellites (!)
    t3 = finder.Search_TLE_Data("cosmos")

    # Calculate the alt/az (degrees) at the time intervals specified for all
    # the satellites passed in. Outputs in the format [<tle_Obj>, <alt>, <az>]
    pdata = finder.Calculate_Passes(t3)

    #finder.Plot_Passes()

    viable_Passes = finder.Filter_Passes(0)
    finder.Print_Pass_List()
    finder.Save_Pass_List()

    finder.Plot_Good_Passes()
