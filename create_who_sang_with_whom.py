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
        minutes.id as minutes_number
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
        lead = {
            "leader": leader,
            "singing": singing,
            "location": location,
            "date": date_string,
            "id": minutes_number,
        }
        list_of_leaders.append(lead)
    return list_of_leaders


infos = get_leaders_and_minutes_info()

# create a index for each singing, which is (singing, location, corrected_date_string, date)
index_to_singing = {}
leader_to_singings = {}

for lead in infos:
    singing_key = lead.get('id')
    singing = index_to_singing.get(singing_key)
    if singing is None:
        singing = {k: v for k, v in lead.items() if k != 'leader'}
        index_to_singing[singing_key] = singing

    leader_key = lead.get('leader')
    singings = leader_to_singings.get(leader_key)
    if singings is None:
        singings = [singing_key]
        leader_to_singings[leader_key] = singings
    else:
        if singing_key not in singings:
            singings.append(singing_key)

# create a big ol' object with all of this information
who_sang_with_whom = {}
who_sang_with_whom['index_to_singing'] = index_to_singing
who_sang_with_whom['leader_to_singings'] = leader_to_singings

# output it as json

print(json.dumps(who_sang_with_whom))
