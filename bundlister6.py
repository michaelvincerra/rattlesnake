from jinja2 import Environment, FileSystemLoader, Template
import jinja2
import os
import re

'''

    [x] Iterate over the files in the bundles directory. Note: Use variable assigned above after os.walk($var...)  
    [x] For each file, extract the value of str that appears to the right of [TITLE]:, and [DESCRIPTION]:
    [x] Create a table with two colums where there is a style sheet, two column headers (USE JINJA) 
    [x] Output this table as an HTML page: bundles.html 
    [x] Play with Jinja template and assure it builds correctly. Create actual template and figure out
        the data structure that works in it. 
    [x] Extract the URL from GitHub (use os.walk()?) and insert <a> tags around 'title' 
    [] Also, extract the value `include` values
        # Refine regex capture group!
        # Need to use .groups() 0,1 correctly to capture all instances of PATTERN3 match. 
    [] Create a function that downloads all data from the GITHUB_BASE URI.    
    [] Create a command that clones github file: 
    `git clone https://github.com/clearlinux/clr-bundles/tree/master/bundles`; then assign a variable to this.
    [] [26] Learn os.walk() and the tuple set that results

    [] Include the Pundles with the GITHUB_BASE URI 
    [] Assign to a variable the result of 'includes' for other bundles
    
'''

import os, re, urllib
import jinja2
from jinja2 import Environment, FileSystemLoader, Template
from pprint import pprint

GITHUB_BASE="https://github.com/clearlinux/clr-bundles/tree/master/bundles/"

PATTERN1 = re.compile(r"#\s?\[TITLE]:\w?(.*)")
PATTERN2 = re.compile(r"#\s?\[DESCRIPTION]:\w?(.*)")
# PATTERN3 = re.compile(r"""include(.*)\n""")
PATTERN3 = re.compile(r"\(([^()]*|include)\)", re.MULTILINE)


# PATTERN3 = re.compile(r"""#\s?include\w?(.*)""")

def extractor(lines): 
     # stores return value in 'lines' param so it's callable in receiving function.
    data_title = "title"
    data_desc = "description"
    url = "url"
    include_list = []

    for i in lines:
        title = PATTERN1.match(i)
        desc = PATTERN2.match(i)
        includes = PATTERN3.findall(i)
 
        if title:
            data_title = title.groups(0)[0].strip()
        #. groups() returns a tuple with all the subgroups of the match, 
        # from one to however many there are in the pattern. 
        # print(data_title)
        if desc: 
            data_desc = desc.groups(0)[0].strip()
        # [0] Explain why the splice [0]
        #. groups() returns a tuple with all the subgroups of the match, from one to however many there are in the pattern. 
        #  print(data_desc)   
        if url: 
            url = os.path.join(GITHUB_BASE, data_title)
        if includes:
            include_text = includes[0].strip("()")
            include_list.append(include_text)


    return {"data_desc": data_desc, "data_title":data_title, "url": url, "include_list": include_list}
    # return statement sets  up a dictionary with keys as 'strings' 
    # whose values, data desc, data_title, are the  

def bundle_lister():
    data = []
    for root, dirs, files in os.walk("/Users/michaelevan/temp/intel_python/clr-bundles/bundles", topdown=False):
        for name in files:
            with open(os.path.join(root, name)) as file_obj:
                lines = file_obj.readlines()
                data.append(extractor(lines))

    loader = jinja2.FileSystemLoader(searchpath='./') # Directory where template is; to be changed to URL path
    env = jinja2.Environment(loader=loader)
    template = env.get_template('template.html')
    output = template.render(data=data)
    with open('bundles01.html', 'w') as file:
        file.write(output)

bundle_lister()


