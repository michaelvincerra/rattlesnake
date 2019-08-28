#!/usr/bin/python

import io
import os
import re
import urllib
import jinja2
from jinja2 import Environment, FileSystemLoader, Template
import git
from operator import itemgetter
from datetime import datetime 

GITHUB_BASE = "https://github.com/clearlinux/clr-bundles/tree/master/bundles/"

PATTERN1 = re.compile(r"#\s?\[TITLE]:\s?(.*)")
PATTERN2 = re.compile(r"#\s?\[DESCRIPTION]:\s?(.*)")
PATTERN3 = re.compile(r"(?<=include)\(.*\)", re.MULTILINE)
PATTERN4 = re.compile(r"(#\s?\[STATUS]):\s?(.*)")

def extractor(lines):
    bundle_title = "title"
    data_desc = "description"
    url = "url"
    include_list = []
    include_unique = []
    status = "status"

    for i in lines:
        title = PATTERN1.match(i)
        desc = PATTERN2.match(i)
        includes = PATTERN3.findall(i)
        curr_status = PATTERN4.match(i)

        if title:
            bundle_title = title.groups(0)[0].strip()
        if desc:
            data_desc = desc.groups(0)[0].strip()
        if url:
            url = os.path.join(GITHUB_BASE, bundle_title)
        if curr_status:
            status = curr_status.group(2)

        if includes:
            include_text = includes[0].strip("()")
            include_list.append(include_text)
            include_unique = set(include_list)
    return {"title": bundle_title, "data_desc": data_desc, "include_list": include_unique, "url": url, "status": status}

def main():
    data = []
    try:
        git.Git("./cloned_repo/").clone("https://github.com/clearlinux/clr-bundles.git")
    except:
        pass
    for root, dirs, files in os.walk("./cloned_repo/clr-bundles/bundles", topdown=False):
        for name in files:
            with open(os.path.join(root, name)) as file_obj:
                lines = file_obj.readlines()
                data.append(extractor(lines))
    filtered = list(filter(lambda x: x.get('title'), data))

    sortedData = sorted(filtered, key=lambda x:x['title'].lower())
    #ALT sortedData2 = sorted(sortedData, key=itemgetter('title'))
    loader = jinja2.FileSystemLoader(searchpath='./')
    env = jinja2.Environment(loader=loader)
    template = env.get_template('template.html')
    template.globals['now'] = datetime.utcnow

    output = template.render(data=sortedData, now=datetime.utcnow())
    with io.open('bundles.html', 'w') as file:
        file.write(output)   
          
if __name__ == "__main__":
    main()
    