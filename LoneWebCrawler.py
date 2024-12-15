from WebCrawler import WebCrawler
import urllib.parse as urlp

class LoneWebCrawler(WebCrawler):
    def __init__(self, start_url):
        super().__init__(start_url)

        self.authority = urlp.urlparse(start_url).netloc

    def filter(self, url_l):
        # Filter already visited and sites already planned to visit
        url_l = [url for url in url_l
            if url not in self.visited and url not in self.tovisit
        ]

        # Removing banlisted url
        url_l = [urlp.urlparse(url) for url in url_l]
        for ban_url in self.banlist:
            url_l = [url for url in url_l if not(url.netloc == ban_url[0] and url.path == ban_url[1])]

        # Remove url from other authority
        url_l = [url for url in url_l if url.netloc == self.authority]
        url_l = [urlp.urlunparse(url) for url in url_l]

        return url_l

crawl = LoneWebCrawler("https://en.wikipedia.org")
crawl.crawl()
