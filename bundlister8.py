import os, re, urllib
import jinja2
from jinja2 import Environment, FileSystemLoader, Template
import git


# Next steps: 
#   Write regex to incorporate all alphabetical items from the pundles#   
#   Combine above array with the bundles
#   Sort all combined items alphabetically.
#   Write if/else condition in the template logic to show bundle and/or pundle    
#   Revise directory structure relative to Makefile in bundle_lister() function. 

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

    return {"data_desc": data_desc, "data_title":data_title, "url": url, "include_list": include_list}

def pundler(puns):
    pundle_title = ["pundle_title"]
    url = "url"
    pundle_list = []

    for i in puns: 
        pundle = PATTERN4.findall(i)
        if pundle: 
            pundle_title = pundle[0]
            pundle_list.append(pundle_title)
        if url: 
            url = PUNDLES
    return {"pundle_title": pundle_title, "url": url }


def bundler():# 
    git.Git("/Users/michaelevan/temp/intel_python/rattlesnake/cloned_repo/").clone("https://github.com/clearlinux/clr-bundles.git")
    data = []
    for root, dirs, files in os.walk("/Users/michaelevan/temp/intel_python/rattlesnake/cloned_repo/clr-bundles/bundles", topdown=False):
        for name in files:
            with open(os.path.join(root, name)) as file_obj:
                lines = file_obj.readlines()
                data.append(extractor(lines))
    
    # # titles_and_pundles = data_title.join(pundles_desc).sorted()
    # "data_title":titles_and_pundles,
    
    # for root, dirs, files in os.walk("/Users/michaelevan/temp/intel_python/rattlesnake/cloned_repo/clr-bundles/packages", topdown=False):
    #     for name in files:
    #         with open(os.path.join(root, name)) as file_obj:
    #             lines = file_obj.readlines()
    #             data.append(pundler(lines))

    loader = jinja2.FileSystemLoader(searchpath='./') 
    env = jinja2.Environment(loader=loader)
    template = env.get_template('template.html')
    output = template.render(data=data)
    with open('bundles01.html', 'w') as file:
        file.write(output)

bundler()


