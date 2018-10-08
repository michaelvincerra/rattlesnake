import os, re, urllib
import jinja2
from jinja2 import Environment, FileSystemLoader, Template
import git
# from collections import defaultdict


# Next steps: 
#   Write if/else condition in the template logic to show bundle and/or pundle    
#   Revise directory structure relative to Makefile in bundle_lister() function. 
#   Write .sh script to call Python script and delete cloned_repo

GITHUB_BASE="https://github.com/clearlinux/clr-bundles/tree/master/bundles/"
PUNDLES="https://github.com/clearlinux/clr-bundles/blob/master/packages"

PATTERN1 = re.compile(r"#\s?\[TITLE]:\w?(.*)")
PATTERN2 = re.compile(r"#\s?\[DESCRIPTION]:\w?(.*)")
PATTERN3 = re.compile(r"\(([^()]*|include)\)", re.MULTILINE)
PATTERN4 = re.compile(r"""^((?:(?!#).*)+)\n""", re.MULTILINE)
# PATTERN4 = re.compile(r"^((?!#).)*$", re.MULTILINE)


def extractor(lines): 
    data_title = "title"
    data_desc = "description"
    url = "url"
    include_list = []
    # pundles = "pundles"

    for i in lines:
        title = PATTERN1.match(i)
        desc = PATTERN2.match(i)
        includes = PATTERN3.findall(i)
        # pundles_desc = PATTERN4.findall(i)

        if title:
            data_title = title.groups(0)[0].strip()
        if desc: 
            data_desc = desc.groups(0)[0].strip()
        if url: 
            url = os.path.join(GITHUB_BASE, data_title)
        if includes:
            include_text = includes[0].strip("()")
            include_list.append(include_text)

    return {"data_title":data_title, "data_desc": data_desc, "include_list": include_list, "url": url}

def pundler():
    with open("/Users/michaelevan/temp/intel_python/rattlesnake/cloned_repo/clr-bundles/packages") as file_obj:
        lines = file_obj.readlines()
        pundle_title = ["pundle_title"]
        purl = "purl" # p+url = URL for pundle; constant
        pundle_list = []
        
        for i in lines: 
            pundle = PATTERN4.findall(i)

            if pundle: 
                pundle_title = pundle[0].strip()
                pundle_list.append(pundle_title)

            purl = PUNDLES

    return {"pundle_list": pundle_list, "purl": purl }


def bundler():
    git.Git("/Users/michaelevan/temp/intel_python/rattlesnake/cloned_repo/").clone("https://github.com/clearlinux/clr-bundles.git")
    data = []
    # bundle_only = []


    for root, dirs, files in os.walk("/Users/michaelevan/temp/intel_python/rattlesnake/cloned_repo/clr-bundles/bundles", topdown=False):
        for name in files:
            with open(os.path.join(root, name)) as file_obj:
                lines = file_obj.readlines()
                data.append(extractor(lines))
    data.append(pundler())
    print(data)
 
    loader = jinja2.FileSystemLoader(searchpath='./') 
    env = jinja2.Environment(loader=loader)
    template = env.get_template('template.html')
    output = template.render(data=data)
    with open('bundles01.html', 'w') as file:
        file.write(output)


def combinator(): 
    """
    Output an alphabetized dictionary to be called by key in template.html
    """
    combo_title = []
    bundle_title = "bundle_title"
    pundle_title = "pundle_title"

    combo_title.append(bundler())

    for d in data:
        if 'data_title':
            bundle_title = str(d.get('data_title'))
            combo_title.append(bundle_title)

    for p in data:
        if 'pundle_list':
    #     # if 'pundle_list' is not None and 'pundle_list' in data:            
            pundle_title = p.get('pundle_list') 
 
    puns = list(pundle_title)
    for pun in puns:
        combo_title.append(pun) 

    combo_title.sort()
    
    return {"combo_title": combo_title}



bundler()



