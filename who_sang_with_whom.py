#!/usr/bin/env python
# encoding: utf-8

import difflib
import json
import sys


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

    # each singing is separated by a tab. split
    shared_singings = [singing.split('\t') for singing in shared_singings]
    # the last element is the date, so sort by that
    shared_singings.sort(key=lambda x: x[-1])
    # make each shared singing an object
    shared_singings = [{'singing': singing[0], 'location': singing[1], 'date': singing[3]} for singing in shared_singings]
    return {'singers': corrected_leaders, 'singings': shared_singings}


def main():
    leaders = sys.argv[1:]
    print(json.dumps(shared_singings(leaders)))

if __name__ == '__main__':
    main()
