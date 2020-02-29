#!/usr/bin/env python

# -*- coding: utf-8 -*-
#
#       prayertime.py
#       
#       Copyright 2010 ahmed youssef <xmonader@gmail.com>
#       
#       This program is free software you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.



from __future__ import print_function
__author__ = "Ahmed Youssef"
__all__ = ['Season', 'Calendar', 'Prayertime', 'Mazhab', \
        'as_pytime', 'as_pydatetime']

from math import degrees, radians, atan, asin, acos, cos, sin, tan 
from datetime import date, datetime
from time import strptime

def remove_duplication(var):
    ##BETTER WAY?
    if var > 360:
        var /= 360   
        var -= int(var) 
        var *= 360
    return var
          
class Season(object):
    Winter, Summer = 0, 1

class Calendar(object):
    UmmAlQuraUniv, \
    EgyptianGeneralAuthorityOfSurvey,\
    UnivOfIslamicSciencesKarachi,\
    IslamicSocietyOfNorthAmerica,\
    MuslimWorldLeague = range(5)

class Mazhab(object):
    Default, Hanafi = 0, 1

def to_hrtime(var, isAM=False):
    
    """var: double -> human readable string of format "%I:%M:%S %p" """
    
    time = ''
    intvar = int(var) #var is double.
    if isAM:
        if intvar % 12 and intvar % 12 < 12:
            zone = "AM"
        else:
            zone = "PM"
    else:
        zone = "PM"
    
    if intvar > 12:
        time += str(intvar%12)            
    elif intvar % 12 == 12:
        time += str(intvar)
    else:
        time += str(intvar)

            
    time += ":"
    var -= intvar
    var *= 60
    minute = int(var)
    time += str(minute)
        
    time += ":"
        
    var -= int(var)
    var *= 60
    sec = int(var)
    time += str(sec)
    time += " "
        
    time += zone
        
    return time

def as_pytime(string_to_parse, fmt="%I:%M:%S %p"):
    """returns time.tm_struct by parsing string_to_parse."""
    return strptime(string_to_parse, fmt)
    
def as_pydatetime(d, ts):
    """returns a datetime object.
            d: date object
            ts: tm_struct
    """
    return datetime(year=d.year, month=d.month, day=d.day, \
                    hour=ts.tm_hour, minute=ts.tm_min, second=ts.tm_sec)
   
class Coordinate(object):
    
    def __init__(self, longitude, latitude, zone):
        """
            Describe a place by its longitude, latitude, and zone.
        """
        
        self.longitude = longitude
        self.latitude = latitude
        self.zone = zone
        
class Prayertime(object):
        
    def __init__(self, longitude, latitude, zone, \
                 year, month, day, \
                 cal=Calendar.UmmAlQuraUniv, mazhab=Mazhab.Default,  season=Season.Winter):

        self.coordinate = Coordinate(longitude, latitude, zone)
        self.date = date(year, month, day)
        self.calendar = cal
        self.mazhab = mazhab
        self.season = season
        self._shrouk = None
        self._fajr = None
        self._zuhr = None
        self._asr = None
        self._maghrib = None
        self._isha = None
        self.dec = 0
        
    def shrouk_time(self):
        """Gets the time of shrouk."""
        
        fmt = to_hrtime(self._shrouk, True)
        return fmt
            
    def fajr_time(self):
        """Gets the time of fajr."""
        
        fmt = to_hrtime(self._fajr, True)
        return fmt
        
    def zuhr_time(self):
        """Gets the time of zuhr."""

        fmt = to_hrtime(self._zuhr, True)
        return fmt


    def asr_time(self):
        """Gets the time of asr."""
        
        fmt = to_hrtime(self._asr)
        return fmt
    
    def maghrib_time(self):
        """Gets the time of maghrib"""
        
        fmt = to_hrtime(self._maghrib)
        return fmt

    def isha_time(self):
        """Gets the time of isha"""
        
        fmt = to_hrtime(self._isha)
        return fmt

    def calculate(self):
        """Calculations of prayertimes."""
        
        year = self.date.year
        month = self.date.month
        day = self.date.day
        longitude = self.coordinate.longitude
        latitude = self.coordinate.latitude
        zone = self.coordinate.zone
        julian_day = (367*year)-int(((year+int((month+9)/12))*7)/4)+int(275*month/9)+day-730531.5
        sun_length = 280.461+0.9856474*julian_day
        sun_length = remove_duplication(sun_length)
        middle_sun = 357.528+0.9856003*julian_day
        middle_sun = remove_duplication(middle_sun)
        
        lamda = sun_length+1.915*sin(radians(middle_sun))+0.02*sin(radians(2*middle_sun))
        lamda = remove_duplication(lamda)
        
        obliquity = 23.439-0.0000004*julian_day
    
        alpha = degrees(atan(cos(radians(obliquity))*tan(radians(lamda))))
        
        if 90 < lamda < 180 :
            alpha += 180
        elif 100 < lamda < 360:
            alpha += 360
    
        ST = 100.46+0.985647352*julian_day
        ST = remove_duplication(ST)
    
        self.dec = degrees(asin(sin(radians(obliquity))*sin(radians(lamda))))
    
        noon = alpha-ST
    
        if noon < 0:
            noon += 360
    
        UTNoon = noon-longitude
        local_noon = (UTNoon/15)+zone
        zuhr = local_noon                #Zuhr Time.
        maghrib = local_noon+self._equation(-0.8333)/15      # Maghrib Time
        shrouk = local_noon-self._equation(-0.8333)/15      # Shrouk Time
    
        fajr_alt = 0
        isha_alt = 0
        
        if  self.calendar == Calendar.UmmAlQuraUniv:
            fajr_alt = -19
        elif self.calendar == Calendar.EgyptianGeneralAuthorityOfSurvey:
            fajr_alt = -19.5
            isha_alt = -17.5
        elif self.calendar == Calendar.MuslimWorldLeague:
            fajr_alt = -18
            isha_alt = -17
        elif self.calendar == Calendar.IslamicSocietyOfNorthAmerica:
            fajr_alt = isha_alt = -15
        elif self.calendar == Calendar.UnivOfIslamicSciencesKarachi:
            fajr_alt = isha_alt = -18
    
    
        fajr = local_noon-self._equation(fajr_alt)/15  # Fajr Time
        isha = local_noon+self._equation(isha_alt)/15  # Isha Time
    
        if self.calendar == Calendar.UmmAlQuraUniv :
            isha = maghrib+1.5
            
        asr_alt = 0
        
        if self.mazhab == Mazhab.Hanafi :
            asr_alt = 90 - degrees(atan(2+tan(radians(abs(latitude - self.dec)))))
        else:
            asr_alt = 90 - degrees(atan(1 + tan(radians(abs(latitude - self.dec)))))
            
        asr = local_noon+self._equation(asr_alt)/15   # Asr Time.
        
        #Add one hour to all times if the season is Summmer.
        if self.season == Season.Summer:
            fajr += 1
            shrouk += 1
            zuhr += 1
            asr += 1
            maghrib += 1
            isha += 1
    
        self._shrouk = shrouk
        self._fajr = fajr
        self._zuhr = zuhr
        self._asr = asr
        self._maghrib = maghrib
        self._isha = isha
    
        
    def _equation(self, alt):
        
        #return RadToDeg*acos((sin(alt*DegToRad)-sin(self.dec*DegToRad)*sin(self.coordinate.latitude*DegToRad))/(cos(self.dec*DegToRad)*cos(self.coordinate.latitude*DegToRad)))
        return degrees( acos( (sin(radians(alt)) - sin(radians(self.dec)) * sin(radians(self.coordinate.latitude)))/(cos(radians(self.dec))*cos(radians(self.coordinate.latitude)))))
        
    def report(self):
        """Simple report of all prayertimes."""
        print(self.fajr_time())
        print(self.shrouk_time())
        print(self.zuhr_time())
        print(self.asr_time())
        print(self.maghrib_time())
        print(self.isha_time())
    
    def report_full(self):
        """Simple report of all prayertimes."""
        
        print(as_pydatetime(self.date, as_pytime(self.fajr_time())).strftime("%I:%M:%S %p"))
        print(as_pydatetime(self.date, as_pytime(self.shrouk_time())).strftime("%I:%M:%S %p"))
        print(as_pydatetime(self.date, as_pytime(self.zuhr_time())).strftime("%I:%M:%S %p"))
        print(as_pydatetime(self.date, as_pytime(self.asr_time())).strftime("%I:%M:%S %p"))
        print(as_pydatetime(self.date, as_pytime(self.maghrib_time())).strftime("%I:%M:%S %p"))
        print(as_pydatetime(self.date, as_pytime(self.isha_time())).strftime("%I:%M:%S %p"))

if __name__=="__main__":
    
    pt = Prayertime(11.57306412752331, 48.1844202348964, 2, 2015, 10, 23)
    pt.calculate()
    pt.report()
    pt.report_full()

#GPSvalues(latitude='48.1844202348964', longitude='11.57306412752331', altitude='516', accuracy='65', altitudeAccuracy='162', heading='null', speed='null', timestamp='23. Oktober 2015 um 16:39:36 MESZ')