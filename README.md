# web-crawler

This repo contains a simple implementation of a web-crawler.

## Index

- Web crawler
- Design decisions
- Technologies
- Challenges
- Limitations

## Web crawler

A web crawler is a program that browses the Internet.
A possible approach to implement this is shown as follows:
- Start with a root URL
- Visit page
- Collect URL mentioned in page
- Perform step 2 with the new URL

## Design decisions

This web crawler serves no purposes other than to visit links and to showcase how we can quickly jump from subjects to subject.
Furthermore, the links visited are only meant to be viewed as they come, and not processed later on. As such, we can accept a full step to take ~1 second.

## Technologies

We use the following Python packages to implement the web-crawler:
- Requests : fetch the pages from a given link
- BeautifulSoup : Parse text and fetch links
- urllib : Perform miscellaneous URL manipulation tasks

## Challenges

The main challenge is bypassing anti-crawler mechanism.
Although it is understandable to have websites be inaccessible and hidden behind a login page, some websites have additional measures, linking to a same template page by modifying the URL query field.

As such, countermeasures are also put into place where we define a banlist containing such pages that attempt to trap our crawler.

## Limitations

Not every websites is accessible by our crawler, only static sites. Furthermore, pages that are hidden behind a login page are also inaccessible, however a list of them is compiled and could be used for a more thorough research.
