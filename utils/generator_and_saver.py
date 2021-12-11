import short_url as su


def generate_short_url(index: int) -> str:
    """
    This function is generate short url for unix timestamp
    :param index:
    :return:
    """
    return su.encode_url(index)


def save_url(long_url: str, short_url: str, _id, db):
    """
    This function is modify long url
    :param long_url:
    :param shortener_url:
    :param db:
    :return:
    """
    db.find_and_modify('url', query={'_id': _id, 'long_url': long_url}, short_url=short_url)
