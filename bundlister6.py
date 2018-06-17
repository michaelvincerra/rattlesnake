import os, re, urllib
import jinja2
from jinja2 import Environment, FileSystemLoader, Template

GITHUB_BASE="https://github.com/clearlinux/clr-bundles/tree/master/bundles/"

PATTERN1 = re.compile(r"#\s?\[TITLE]:\w?(.*)")
PATTERN2 = re.compile(r"#\s?\[DESCRIPTION]:\w?(.*)")
PATTERN3 = re.compile(r"\(([^()]*|include)\)", re.MULTILINE)

def extractor(lines): 
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
        if desc: 
            data_desc = desc.groups(0)[0].strip()
        if url: 
            url = os.path.join(GITHUB_BASE, data_title)
        if includes:
            include_text = includes[0].strip("()")
            include_list.append(include_text)
            
    return {"data_desc": data_desc, "data_title":data_title, "url": url, "include_list": include_list}
 

def bundle_lister():
    data = []
    for root, dirs, files in os.walk("/Users/michaelevan/temp/intel_python/clr-bundles/bundles", topdown=False):
        for name in files:
            with open(os.path.join(root, name)) as file_obj:
                lines = file_obj.readlines()
                data.append(extractor(lines))

    loader = jinja2.FileSystemLoader(searchpath='./') 
    env = jinja2.Environment(loader=loader)
    template = env.get_template('template.html')
    output = template.render(data=data)
    with open('bundles01.html', 'w') as file:
        file.write(output)

bundle_lister()


