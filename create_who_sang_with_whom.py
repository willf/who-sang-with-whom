#!/usr/bin/env python
# encoding: utf-8

import json
import re
import sqlite3
from datetime import datetime


def open_db():
    conn = sqlite3.connect("minutes.db")
    return conn

def get_leaders_and_minutes_info():
    list_of_leaders = []
    query = """
    SELECT distinct
	    leaders.name as leader,
	    minutes.name as singing,
	    minutes.Location as location,
	    minutes.Date as date_string,
        minutes.id-1 as minutes_number
    FROM
	    leaders
    JOIN
	    song_leader_joins ON leaders.id = song_leader_joins.leader_id
    JOIN
	    minutes ON song_leader_joins.minutes_id = minutes.id
;
    """
    db = open_db()
    cursor = db.execute(query)
    for (leader, singing, location, date_string, minutes_number) in cursor:
        corrected_date_string = correct_date_string(date_string)
        parsed = parse_date_string(corrected_date_string)
        list_of_leaders.append((leader, singing, location, corrected_date_string, parsed.strftime('%Y-%m-%d'), minutes_number))
    return list_of_leaders

def find_first_month(string):
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for i, month in enumerate(months):
        if re.search(month, string):
            return i+1
    return None

def find_first_day(string):
    pattern = r'\b\d{1,2}\b'
    match = re.search(pattern, string)
    if match:
        return int(match.group())
    else:
        return None

def find_first_year(string):
    pattern = r'\b\d{4}\b'
    match = re.search(pattern, string)
    if match:
        return int(match.group())
    else:
        return None

def parse_date_string(date_string):
    month = find_first_month(date_string)
    day = find_first_day(date_string)
    year = find_first_year(date_string)
    if month and day and year:
        return datetime(year, month, day)
    else:
        return None

def correct_date_string(date_string):
    corrections = {}
    corrections["February 5, l995"] = "February 5, 1995"
    corrections["Monday, July 5"] = "Monday, July 5, 2010"
    corrections["Saturday, April 26, l997"] = "Saturday, April 26, 1997"
    corrections["Saturday, July 28, 20001"] = "Saturday, July 28, 2001"
    corrections["Saturday, June I9, 2004"] = "Saturday, June 19, 2004"
    corrections["Saturday, May 20, l995"] = "Saturday, May 20, 1995"
    corrected = corrections.get(date_string)
    if corrected:
        return corrected
    else:
        return date_string

def make_key(singing, location, date_string, date, minutes_number):
    # return as a string
    return "\t".join([singing, location, date_string, date, str(minutes_number)])

infos = get_leaders_and_minutes_info()

# create a index for each singing, which is (singing, location, corrected_date_string, date)
index_to_singing = {}
singing_to_index = {}

for (_, singing, location, date_string, date, minutes_number) in infos:
    key = make_key(singing, location, date_string, date, minutes_number)
    index = singing_to_index.get(key)
    if index is None:
        index = minutes_number
        singing_to_index[key] = index
        index_to_singing[index] = key


# create an index from each leader to a list of all the singings they led
leader_to_singings = {}
for (leader, singing, location, date_string, date, minutes_number) in infos:
    key = make_key(singing, location, date_string, date, minutes_number)
    index = singing_to_index[key]
    singings = leader_to_singings.get(leader)
    if singings is None:
        singings = [index]
        leader_to_singings[leader] = singings
    else:
        if index not in singings:
            singings.append(index)

# create a big ol' object with all of this information
who_sang_with_whom = {}
who_sang_with_whom['index_to_singing'] = index_to_singing
who_sang_with_whom['leader_to_singings'] = leader_to_singings

# output it as json

print(json.dumps(who_sang_with_whom))
