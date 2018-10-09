`bundle_lister.py` is a Python (3.6.0) web scraper that clones the clr-bundles directory, https://github.com/clearlinux/clr-bundles, parses content in the bundles directory and in packages file with regex,
and uses Jinja2 to output a file: bundles.html. This html file is a table that appears in webpage. The `bundle_liste.py` program will be invoked in a bash script upon daily builds of the website. `bundle_lister.py` automates documentation so it shows current bundles and packages per the latest updates on the clr-bundles GitHub repository.  

To run `bundle_lister.py`, in the terminal, enter: `python bundle_lister.py`.

Note: A successful build should show a file named `bundles.html`. Bundles and pundles (aka, 'packages'), appear alphabetically in a table in `bundles.html`. 
In a future iteration, this program  will be invoked in a bash script as noted above.  
