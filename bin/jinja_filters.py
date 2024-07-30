from bs4 import BeautifulSoup
from markdown import markdown
from markupsafe import Markup
from slugify import slugify


def render_markdown_filter(text, include_classes=True, make_safe=True):
    if text is None:
        return ""
    soup = BeautifulSoup(markdown(text), "html.parser")
    if include_classes:
        _add_html_attrs(soup)
    if make_safe:
        return Markup(soup)
    else:
        return soup


def _add_html_attrs(soup):
    for tag in soup.select("p"):
        tag["class"] = "gwg-body"
    for tag in soup.select("h1, h2, h3, h4, h5"):
        # sets the id to a 'slugified' version of the text content
        tag["id"] = slugify(tag.getText())
    for tag in soup.select("h1"):
        tag["class"] = "gwg-heading-xl"
    for tag in soup.select("h2"):
        tag["class"] = "gwg-heading-l"
    for tag in soup.select("h3"):
        tag["class"] = "gwg-heading-m"
    for tag in soup.select("h4"):
        tag["class"] = "gwg-heading-s"
    for tag in soup.select("ul"):
        tag["class"] = "gwg-list gwg-list--bullet"
    for tag in soup.select("a"):
        tag["class"] = "gwg-link"
    for tag in soup.select("ol"):
        tag["class"] = "gwg-list gwg-list--number"
    for tag in soup.select("hr"):
        tag["class"] = "gwg-section-break gwg-section-break--l"
