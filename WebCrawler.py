import requests
from bs4 import BeautifulSoup
import urllib.parse as urlp

class WebCrawler:
    def __init__(self, start_url):
        self.visited = []
        self.tovisit = [start_url]

        self.banlist = []

        self.skip_page = {
            "image/png",
            "image/jpeg",
            "application/pdf",
            "application/octet-stream"
        }

        self.max_planned_visit = 1000
        self.save_counter = 100

    def fetch_url(self, html):
        soup = BeautifulSoup(html, "html.parser")
        url_l = []
        for anchor in soup.find_all("a"):
            url_l += [anchor.get("href")]
        url_l = list(set(url_l))
        return url_l

    def get_https_url(self, url_l):
        url_l = [urlp.urlparse(url) for url in url_l]
        url_l = [url for url in url_l
            if url.fragment == "" and url.scheme in {"", "https"}
        ]
        url_l = [urlp.urlunparse(url) for url in url_l]
        return url_l

    def to_abs_path(self, url_l, visit_url):
        url_l = [urlp.urlparse(url) for url in url_l]
        abs_url_l = [urlp.urlunparse(url) for url in url_l if url.scheme == "https"]
        rel_url_l = [urlp.urljoin(visit_url, urlp.urlunparse(url)) for url in url_l
            if url.scheme == ""
        ]
        return abs_url_l + rel_url_l

    def filter(self, url_l):
        # Filter already visited and sites already planned to visit
        url_l = [url for url in url_l
            if url not in self.visited and url not in self.tovisit
        ]

        # Removing banlisted url
        url_l = [urlp.urlparse(url) for url in url_l]
        for ban_url in self.banlist:
            url_l = [url for url in url_l if not(url.netloc == ban_url[0] and url.path == ban_url[1])]
        url_l = [urlp.urlunparse(url) for url in url_l]

        return url_l

    def visit(self):
        # Set site as visited
        visit_url = self.tovisit[0]
        self.visited += [visit_url]
        self.tovisit = self.tovisit[1:]
        print(f"Visiting {visit_url}")

        # Visit page
        try:
            page = requests.get(visit_url)
        except requests.exceptions.RequestException:
            return None

        # Skip page
        if "content-type" in page.headers:
            if page.headers["content-type"] in self.skip_page:
                return None

        # Parse HTML
        url_l = self.fetch_url(page.content)
        url_l = self.get_https_url(url_l)
        url_l = self.to_abs_path(url_l, visit_url)
        url_l = self.filter(url_l)

        # Limit number of planned visits
        self.tovisit = url_l + self.tovisit
        if (len(self.tovisit) > self.max_planned_visit):
            self.tovisit = self.tovisit[:self.max_planned_visit]

    def can_visit(self):
        if self.tovisit == []:
            print("Crawler is lost")
            return False
        return True

    def crawl(self):
        counter = 0
        while self.can_visit():
            self.visit()
            counter += 1
            if counter % self. save_counter == 0:
                self.save(f"checkpoint/url_checkpoint_{counter}.txt")
            self.check_trap()

    def save(self, filename):
        with open(filename, "w") as f:
            for url in self.visited:
                f.write(f"{url}\n")

    def check_trap(self):
        url_l = {}
        for url in self.visited[-20:]:
            authority = (urlp.urlparse(url).netloc, urlp.urlparse(url).path)
            url_l[authority] = url_l.get(authority, 0) + 1
        for url, n in url_l.items():
            if n >= 5:
                self.banlist += [authority]



