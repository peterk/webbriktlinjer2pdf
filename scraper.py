# -*- coding: utf-8 -*-
import requests
from lxml import html, etree
from lxml.html.clean import Cleaner
import os
import sys
import datetime
#import subprocess


#Some utility methods

def save_doc(filename, doc):
    with open(filename,'w') as f:
        f.write(etree.tostring(doc, method='html', encoding='utf-8'))


def remove_el(doc, css):
    """remove html element from document by css path"""
    els = doc.cssselect(css)
    for el in els:
        el.getparent().remove(el)


def increase_heading_level(doc):

    headings = doc.cssselect("h1")
    headings.extend(doc.cssselect("h2"))
    headings.extend(doc.cssselect("h3"))
    headings.extend(doc.cssselect("h4"))
    headings.extend(doc.cssselect("h5"))

    for heading in headings:
        level = int(heading.tag[1])
        heading.tag = "h%s" % (level + 1)



def remove_heading_links(doc):
    """remove links from <h1><a href='...'> constructs"""

    # find links in headings
    links = doc.cssselect("h2>a")
    links.extend(doc.cssselect("h3>a"))
    links.extend(doc.cssselect("h4>a"))

    for link in links:
        #remove a but retain text content
        etree.strip_tags(link.getparent(),"a")


def clean_doc(content):
    """Clean guidline page from unnecessary HTML"""
    doc = html.document_fromstring(content)

    doc = doc.cssselect("div#main")[0]

    #header
    remove_el(doc, "div.page-header")

    ## drop overview
    remove_el(doc,"div.small-overview")

    ##small-column
    remove_el(doc,"div.small-column")

    # drop here links
    remove_el(doc,"span.here-link")

    # remove links fro headings
    remove_heading_links(doc)

    # remove nav elements etc
    remove_el(doc,"div.main-nav")
    remove_el(doc, "div.footer")
    remove_el(doc, "div#comments-container")
    remove_el(doc, "hr")
    remove_el(doc, "script")
    remove_el(doc, "div.page-footer")

    return doc


def fix_name(doc):
    """Add guidline number to first h1"""
    el = doc.cssselect("h1")[0]
    gnum = "R%s. " % name_from_doc(doc)
    el.text = gnum + el.text


def name_from_doc(doc):
    """Parse doc and make filename"""
    el = doc.cssselect("p.guideline-title")[0]
    para = el.text_content().split("Prio")[0].strip()
    return para.replace("Riktlinje nr ", "").strip()


def clean_principle(content):
    doc = html.document_fromstring(content)
    doc = doc.cssselect("div#main")[0]
    remove_el(doc, "ul.prio-nav")
    increase_heading_level(doc)
    return doc



# set up timestamps
human_now = datetime.datetime.now().isoformat().split(".")[0].replace("T"," ")
now = human_now.replace(":","").replace(" ","T")

# Load result html template
guideline_urls = []
filenames = []
HTML_TEMPLATE = ""

# Load html output template with styles
with file("template.html") as f: HTML_TEMPLATE = f.read()
HTML_TEMPLATE = HTML_TEMPLATE.replace("{now}", human_now)

resultdoc = html.document_fromstring(HTML_TEMPLATE)
principles_root = resultdoc.cssselect("div#principles")[0]
root = resultdoc.cssselect("div#guidelines")[0]
filename = ""


# 0. Get principles
principle_urls = ["http://www.webbriktlinjer.se/principer/tillganglig/", "http://www.webbriktlinjer.se/principer/anvandbar/", "http://www.webbriktlinjer.se/principer/fortroendeingivande/", "http://www.webbriktlinjer.se/principer/effektiv/", "http://www.webbriktlinjer.se/principer/tekniskt-oberoende/", "http://www.webbriktlinjer.se/principer/atkomlig-over-tid/"]

for url in principle_urls:
    print "Getting %s" % url
    resp = requests.get(url)

    doc = clean_principle(resp.content.decode("utf-8"))
    principles_root.append(doc)

print "Added principles"


# 1. get links for guidelines
response = requests.get("http://www.webbriktlinjer.se/riktlinjer/alla-riktlinjer-i-nummerordning/")
doc = html.document_fromstring(response.content)
els = doc.cssselect("ul.nav li a")

if els:
    for item in els:
        url = item.get("href", None)
        if url:
            guideline_urls.append(url)


# 2. get guidelines and create doc
for url in guideline_urls:
    print "Getting %s" % url
    resp = requests.get(url)

    doc = clean_doc(resp.content.decode("utf-8"))
    fix_name(doc)
    remove_el(doc,  "p.guideline-title")
    root.append(doc)


# 3. Write html doc for conversion
filename = "vlwebb-%s.html" % now
save_doc(filename, resultdoc)

print "Wrote %s docs" % len(guideline_urls)

# 4. Use open office to convert to ODF. Check your path to open office executable.
command = "/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to odt:writer8 %s" % filename
os.system(command)

print "Done!"

