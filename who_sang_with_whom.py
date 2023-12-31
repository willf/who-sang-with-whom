#!/usr/bin/env python
# encoding: utf-8

import difflib
import json
import sys

# This is a script that takes a list of leaders and returns a list of
# singings that they have all led at together
# It's a CLI version of the web app
# Usage: python who_sang_with_whom.py leader1 leader2 leader3
# For example: python who_sang_with_whom.py "Will Fitzgerald" "Samuel Sommers" | jq .
# The output is a json object with two keys: singers and singings

def best_match(leader, all_leaders):
    matches = difflib.get_close_matches(leader, all_leaders, 1)
    if len(matches) > 0:
        return matches[0]
    else:
        return None

def safe_index(list, item):
    try:
        return list.index(item)
    except ValueError:
        return -1

def shared_singings(leaders):
    who_sang_with_whom = {}
    # read in the json
    with open('who_sang_with_whom.json', 'r') as f:
        who_sang_with_whom = json.load(f)

    leaders_to_singings = who_sang_with_whom['leader_to_singings']
    all_leaders = leaders_to_singings.keys()
    singings = who_sang_with_whom['index_to_singing']

    # correct the leaders
    corrected_leaders = [best_match(leader, all_leaders) for leader in leaders]

    # if any of the leaders are None, then we can't find a match

    index_of_none = safe_index(corrected_leaders, None)
    if index_of_none != -1:
        return {'singers': leaders, 'singings': [], 'error': 'Could not find a match for ' + leaders[index_of_none]}


    # now we have a list of leaders, and we want to find all the singings they have
    # in common
    indexes = set(leaders_to_singings[corrected_leaders[0]])
    for leader in corrected_leaders[1:]:
        # get the set intersection of the indexes
        indexes = indexes.intersection(leaders_to_singings[leader])

    # now we have a set of indexes, and we want to print out the information
    # for each one
    if len(indexes) == 0:
        return {'singers': corrected_leaders, 'singings': []}
    shared_singings = [singings[str(index)] for index in indexes]

    # the last element is the date, so sort by that
    shared_singings.sort(key=lambda x: x["id"])
    # make each shared singing an object
    return {'singers': corrected_leaders, 'singings': shared_singings}


def main():
    leaders = sys.argv[1:]
    print(json.dumps(shared_singings(leaders)))

if __name__ == '__main__':
    main()
