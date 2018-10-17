`bundle_lister.py` is a Python (3.6.0) web scraper that clones the clr-bundles directory, https://github.com/clearlinux/clr-bundles, parses content in bundles directory and packages file,
and then uses Jinja2 to output a file: bundles.html. This html file is a table that appears in webpage. `bundle_lister.py` will be invoked in a bash script upon daily builds of the website. `bundle_lister.py` automates documentation so it shows current bundles and packages per latest updates to the clr-bundles GitHub repository.  

See `requirements.txt` for modules/packages necessary for environment. 

To run `bundle_lister.py` in the terminal, enter: `python bundle_lister.py`.

Note, you must create a directory called `cloned_repo` in order for this code to work.

Note: A successful build will produce a file named `bundles.html` showing a table of current bundles and pundles (packages) alphabetized. 

In a future iteration, this program  will be invoked from a bash script as noted above.  
