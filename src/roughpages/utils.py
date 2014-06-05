# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import os


def url_to_filename(url):
    """
    Safely translate url to relative filename

    Args:
        url (str): A target url string

    Returns:
        str
    """
    # remove leading/trailing slash
    if url.startswith('/'):
        url = url[1:]
    if url.endswith('/'):
        url = url[:-1]
    # remove pardir symbols to prevent unwilling filesystem access
    url = remove_pardir_symbols(url)
    return url


def remove_pardir_symbols(path, sep=os.sep, pardir=os.pardir):
    """
    Remove relative path symobls such as '..'

    Args:
        path (str): A target path string
        sep (str): A strint to refer path delimiter (Default: `os.sep`)
        pardir (str): A string to refer parent directory (Default: `os.pardir`)

    Returns:
        str
    """
    bits = path.split(sep)
    bits = (x for x in bits if x != pardir)
    return sep.join(bits)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
