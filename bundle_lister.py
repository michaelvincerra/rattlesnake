import os, re, urllib
import jinja2
from jinja2 import Environment, FileSystemLoader, Template
import git
from operator import itemgetter

DATA = []

GITHUB_BASE="https://github.com/clearlinux/clr-bundles/tree/master/bundles/"
PUNDLES="https://github.com/clearlinux/clr-bundles/blob/master/packages"

PATTERN1 = re.compile(r"#\s?\[TITLE]:\w?(.*)")
PATTERN2 = re.compile(r"#\s?\[DESCRIPTION]:\w?(.*)")
PATTERN3 = re.compile(r"\(([^()]*|include)\)", re.MULTILINE)
PATTERN4 = re.compile(r"""^((?:(?!#).*)+)\n""", re.MULTILINE)

def extractor(lines): 
    bundle_title = "title"
    data_desc = "description"
    url = "url"
    include_list = []


    for i in lines:
        title = PATTERN1.match(i)
        desc = PATTERN2.match(i)
        includes = PATTERN3.findall(i)
        
        if title:
            bundle_title = title.groups(0)[0].strip()
        if desc: 
            data_desc = desc.groups(0)[0].strip()
        if url: 
            url = os.path.join(GITHUB_BASE, bundle_title)

        if includes:
            include_text = includes[0].strip("()")
            include_list.append(include_text)

    return {"bundle_title":bundle_title, "data_desc": data_desc, "include_list": include_list, "url": url}


def pundler():
    with open("/Users/michaelevan/temp/intel_python/rattlesnake/cloned_repo/clr-bundles/packages") as file_obj:
        lines = file_obj.readlines()
        pundle_title = ["pundle_title"]
        purl = "purl" # p+url = URL for pundle; constant
        pundle_list = []
        partial_list = []
        pun_title = "pun_title"

        for i in lines: 
            pundle = PATTERN4.findall(i)

            if pundle: 
                pundle_title = pundle[0].strip()
                pundle_list.append(pundle_title)
            print(pundle_list)


        for pun in pundle_list:
            partial_list.append(pun) 

        partial_list = sorted(partial_list)
        
        pun_title  = [pu for pu in pundle_list]

        purl = PUNDLES

    return {"pundle_list": pundle_list, "purl": purl, "partial_list": partial_list, "pun_title" : pun_title }

def bundler():

    git.Git("/Users/michaelevan/temp/intel_python/rattlesnake/cloned_repo/").clone("https://github.com/clearlinux/clr-bundles.git")
    for root, dirs, files in os.walk("/Users/michaelevan/temp/intel_python/rattlesnake/cloned_repo/clr-bundles/bundles", topdown=False):
        for name in files:
            with open(os.path.join(root, name)) as file_obj:
                lines = file_obj.readlines()
                DATA.append(extractor(lines))

    DATA.append(pundler())
    print(DATA)

    loader = jinja2.FileSystemLoader(searchpath='./') 
    env = jinja2.Environment(loader=loader)


    def order_by(queryset, args):
        args = [x.strip() for x in args.split(',')]
        return queryset.order_by(*args)
        
    env.filters['order_by'] = order_by

    template = env.get_template('template.html')
    output = template.render(data=DATA)

    with open('bundles.html', 'w') as file:
        file.write(output)

bundler()

