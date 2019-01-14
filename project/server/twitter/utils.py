import time
from collections import namedtuple
from urllib.parse import quote_plus

from flask import jsonify

from project.server.utils import twtr


class TwitterData:

    def __init__(self):
        self.count = 100
        self.request_results = []
        self.unpacked_results = []

    def timeline_request(self, screen_name, **kwargs):
        self.request_results = twtr.GetUserTimeline(screen_name=screen_name, count=self.count)
        data = self.unpack_data(**kwargs)
        return data

    def search_request(self, search_term, **kwargs):
        search_query = (f"q={quote_plus(search_term)}&count={str(self.count)}")
        self.request_results = twtr.GetSearch(raw_query=search_query)
        data = self.unpack_data(**kwargs)
        return data

    def list_members_request(self, slug, owner_screen_name, **kwargs):
        self.request_results = twtr.GetListMembers(slug=slug, owner_screen_name=owner_screen_name)
        data = self.unpack_data(**kwargs)
        return data

    def unpack_data(self, **kwargs):
        data = []
        for r in self.request_results:
            d = r.AsDict()
            d["timestamp"] = time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.strptime(d["created_at"], "%a %b %d %H:%M:%S +0000 %Y"),
            )
            data.append(d)
        self.unpacked_results = [dict(i, **kwargs) for i in data]
        return self.unpacked_results



def twitter_search(search_term, count) -> list:
    # form_data = request.form
    tweets = TwitterData()
    tweets.count = count
    data = tweets.search_request(search_term)
    return data


def twitter_timeline(screen_name) -> list:
    tweets = TwitterData()
    results = tweets.timeline_request(screen_name=screen_name)
    data = [i['text'] for i in results]
    return data


def twitter_congressional_list():
    chamber_data = [{'chamber': 'house_of_representatives', 'party': 'republican', 'slug': 'house-republicans', 'owner_screen_name': 'HouseGOP'},
                    {'chamber': 'house_of_representatives', 'party': 'democrat', 'slug': 'house-republicans', 'owner_screen_name': 'HouseGOP'},
                    {'chamber': 'senate', 'party': 'republican', 'slug': 'house-republicans', 'owner_screen_name': 'HouseGOP'},
                    {'chamber': 'senate', 'party': 'democrat', 'slug': 'house-republicans', 'owner_screen_name': 'HouseGOP'}]
    congress = []
    for i in chamber_data:
        tweets = TwitterData()
        tmp = tweets.list_members_request(slug=i['slug'], owner_screen_name=i['owner_screen_name'], chamber=i['chamber'], party=i['party'])
        congress = congress + tmp
    return congress
