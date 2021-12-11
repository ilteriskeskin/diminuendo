from bson.objectid import ObjectId
from configs import URI, NAME
from heybooster.helpers.database.mongodb import MongoDBHelper
from collections import Counter


def get_referrer_urls_for_url(url_id):
    with MongoDBHelper(uri=URI, database=NAME) as db:
        return referrer_urls_analyze(db.find_one('url', query={'_id': ObjectId(url_id)}).referrer_url)


def get_countries_for_url(url_id):
    with MongoDBHelper(uri=URI, database=NAME) as db:
        return countries_analyze(db.find_one('url', query={'_id': ObjectId(url_id)}).country)


def referrer_urls_analyze(referrer_urls):
    splitted_url_list = []

    for referrer_url in referrer_urls:
        splitted_url_list.append(referrer_url.split('/')[2])

    analyzed_data = dict(Counter(splitted_url_list))

    return analyzed_data


def countries_analyze(countries):
    splitted_url_list = []

    for country in countries:
        splitted_url_list.append(country)

    analyzed_data = dict(Counter(splitted_url_list))

    return analyzed_data
