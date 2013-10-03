# Standard imports
from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup


SORTBY_RELEVANCE = 99
SORTBY_NAMEASC   = 2
SORTBY_NAMEDESC  = 1
SORTBY_SIZE      = 5
SORTBY_SEEDERS   = 7
SORTBY_LEECHERS  = 9
SORTBY_TYPE      = 13
SORTBY_UPLOADED  = 3

CAT_NONE         = 0
CAT_AUDIO        = 100
CAT_VIDEO        = 200
CAT_APPLICATIONS = 300
CAT_GAMES        = 400
CAT_OTHERS       = 600

def search_torrents(query, page=0, sort_by=SORTBY_SEEDERS, category=CAT_NONE,
                    required_results=10):
    torrent_url = 'http://thepiratebay.org/search/'
    quoted_query = quote(query)
    doc_file = urlopen(torrent_url +
                       quoted_query + '/' +
                       str(page) + '/' +
                       str(sort_by) + '/' +
                       str(category))

    soup = BeautifulSoup(doc_file.read())
    search_results = soup.select('#searchResult')[0]

    torrents = []
    for search_result in search_results.find_all('tr'):
        # If the tr has a class attribute, then it's a theader and skip over it.
        if search_result.attrs:
            continue
        # We don't need the category, hence skipping the first td.
        search_result_tds = search_result.select('td')[1:]
        links = search_result_tds[0].select('a')
        # The first <a> is the title of the torrent.
        title = links[0].string
        # The second <a>'s href is the magnet link.
        magnet = links[1]['href']
        # The second-last <a>'s href is the uploader.
        uploader = links[-2]['href'].split('/')[-1]
        # Uploader attrs is the image inside the second-last <a>.
        # NOTE: Sometimes, the uploader_attrs isn't available.
        try:
            uploader_attrs = [links[-2].img['title']]
        except:
            uploader_attrs = None
        # The next <td>'s string is the number of seeders.
        seeders = search_result_tds[1].string
        # The next <td>'s string is the number of leechers.
        leechers = search_result_tds[2].string
        torrent = {'title'          : title,
                   'magnet'         : magnet,
                   'uploader'       : uploader,
                   'uploader_attrs' : uploader_attrs,
                   'seeders'        : seeders,
                   'leechers'       : leechers}
        torrents.append(torrent)

        if len(torrents) == required_results:
            break

    return torrents
