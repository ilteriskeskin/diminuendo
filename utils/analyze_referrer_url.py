from collections import Counter


def referrer_urls_analyzer(referrer_urls):
    splitted_url_list = []

    for referrer_url in referrer_urls:
        if referrer_url:
            splitted_url_list.append(referrer_url.split('/')[2])

    analyzed_data = dict(Counter(splitted_url_list))

    return analyzed_data


def countries_analyzer(countries):
    countries_list = []

    for country in countries:
        if country:
            countries_list.append(country)

    analyzed_data = dict(Counter(countries_list))

    return analyzed_data
