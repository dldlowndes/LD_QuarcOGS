"""
Trying to calculate apparent doppler for a satellite at a specified ground
location.

This helps https://docs.astropy.org/en/stable/coordinates/satellites.html
"""

import datetime

import astropy
import astropy.coordinates
import astropy.time
import astropy.units
import dateutil
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sgp4.api
import tzlocal


def convert_timestamp(stamp, tz):
    """
    Convert ISO format timestamp into an astropy timestamp object
    """
    stamp = tz.localize(dateutil.parser.parse(stamp))
    return astropy.time.Time(stamp)

sample_tle = ["ISS (ZARYA)",
              "1 25544U 98067A   21127.19945859  .00000523  00000-0  17665-4 0  9992",
              "2 25544  51.6441 185.4559 0002803 329.9462 127.3881 15.48981972282240"]

# Time parameters of simulation
my_tz = tzlocal.get_localzone()
t_start = convert_timestamp("2021-05-07T00:00:00", my_tz)
t_stop = convert_timestamp("2021-05-07T23:00:00", my_tz)
t_step = datetime.timedelta(seconds=30)

# Turn time parameters into a list of every time point to simulate.
# (sgp4 takes julian dates)
utc_Time_Series = []
ti = t_start
while ti <= t_stop:
    utc_Time_Series.append(ti)
    ti = ti + t_step
jd_Range = np.array([x.jd for x in utc_Time_Series])

# Get position and velocity of the satellite for every time step specified.
sat = sgp4.api.Satrec.twoline2rv(sample_tle[1], sample_tle[2])
_, p, v = sat.sgp4_array(jd_Range, np.zeros_like(jd_Range))

# SGP4 gives results in some weird coordinate basis (True Equator
# Mean Equinox frame (TEME)). Get values in the right format to
# convert to something more intelligible and useful.
teme_p = astropy.coordinates.CartesianRepresentation(p * astropy.units.km, xyz_axis=1)
teme_v = astropy.coordinates.CartesianDifferential(v * (astropy.units.km / astropy.units.s), xyz_axis=1)

# Put the coordinates into astropy, which can convert between bases
# using International Terrestrial Reference System (ITRS) coordinates.
teme = astropy.coordinates.TEME(teme_p.with_differentials(teme_v), obstime=utc_Time_Series)
itrs = teme.transform_to(astropy.coordinates.ITRS(obstime=utc_Time_Series))

here = astropy.coordinates.EarthLocation(lat=51.4538,
                                         lon=-2.5973,
                                         height=71 * astropy.units.m)
observer = astropy.coordinates.AltAz(location=here,
                                     obstime=utc_Time_Series)

view = itrs.transform_to(observer)

plt.rcParams["timezone"] = my_tz
x_data = [x.plot_date for x in utc_Time_Series]
fig1, ax1a = plt.subplots()
ax1a.xaxis_date(my_tz)
fmt = matplotlib.dates.DateFormatter("%H:%M")
ax1a.xaxis.set_major_formatter(fmt)
ax1a.plot(x_data,
         view.alt,
         color="red")
ax1a.set_ylim(-90,90)
ax1a.axhline(0)
ax1b = ax1a.twinx()
ax1b.plot(x_data,
         view.radial_velocity,
         color="blue")
ax1b.set_ylim(-10, 10)
#fig1.show()

# wavelength_receiver / wavelength_source = sqrt((1+beta)/(1-beta))
# frequency_source / frequency_receiver = sqrt((1+beta)/(1-beta))
# beta = v/c
wavelength = 785 * astropy.units.nm
repetition = 100 * astropy.units.kHz
beta = view.radial_velocity / astropy.constants.c
factor = np.sqrt((1 + beta) / (1 - beta))
wavelength_apparent = (wavelength * factor).value
repetition_apparent = ((1 + beta) * repetition).value

fig2, ax2a = plt.subplots()
ax2a.xaxis.set_major_formatter(fmt)
ax2a.plot(x_data,
          wavelength_apparent,
          color="red")
ax2a.set_ylim(784.5, 785.5)
ax2a.axhline(0)
ax2b = ax2a.twinx()
ax2b.plot(x_data,
          repetition_apparent,
          color="blue")
ax2b.set_ylim(99.99, 100.01)
fig2.show()
