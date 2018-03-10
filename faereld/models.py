# -*- coding: utf-8 -*-

"""
faereld.models
--------------

This module models the data structure used within faereld, which consists of:
AREA   :: The category of the time tracked
OBJECT :: The specific object or project tracked
START  :: The datetime the task was started
END    :: The datetime the task was finished

The START and END fields can either use the Gregorian datetime (by default),
which returns the standard python datetime object. Or it can use the Wending
datetime, which returns a Wending object as defined in Datarum.
"""

from wisdomhord import Bisen, Sweor, String, Wending, DateTime

class FaereldWendingEntry(Bisen):

  __invoker__ = 'Færeld'
  __description__ = 'Productive task time tracking data produced by Færeld'

  col1 = Sweor('AREA',   String)
  col2 = Sweor('OBJECT', String)
  col3 = Sweor('START',  Wending)
  col4 = Sweor('END',    Wending)


class FaereldDatetimeEntry(Bisen):

  __invoker__ = 'Færeld'
  __description__ = 'Productive task time tracking data produced by Færeld'

  col1 = Sweor('AREA',   String)
  col2 = Sweor('OBJECT', String)
  col3 = Sweor('START',  DateTime)
  col4 = Sweor('END',    DateTime)
