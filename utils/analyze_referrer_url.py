from collections import Counter


def referrer_urls_analyzer(referrer_urls):
    splitted_url_list = []

    for referrer_url in referrer_urls:
        splitted_url_list.append(referrer_url.split('/')[2])

    analyzed_data = dict(Counter(splitted_url_list))

    return analyzed_data


def countries_analyzer(countries):
    splitted_url_list = []

    for country in countries:
        splitted_url_list.append(country)

    analyzed_data = dict(Counter(splitted_url_list))

    return analyzed_data
