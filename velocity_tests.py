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


def convert_timestamp(stamp):
    my_tz = tzlocal.get_localzone()
    stamp = my_tz.localize(dateutil.parser.parse(stamp))
    return astropy.time.Time(stamp)  


sample_tle = ["ISS (ZARYA)",
              "1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927",
              "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537"]

t_start = convert_timestamp("2021-04-05T09:00:00")
t_stop = convert_timestamp("2021-04-05T21:00:00")
t_step = datetime.timedelta(minutes=1)

utc_Time_Series = []
ti = t_start
while ti <= t_stop:
    utc_Time_Series.append(ti)
    ti = ti + t_step
jd_Range = np.array([x.jd for x in utc_Time_Series])

sat = sgp4.api.Satrec.twoline2rv(sample_tle[1], sample_tle[2])
e, p, v = sat.sgp4_array(jd_Range, np.zeros_like(jd_Range))