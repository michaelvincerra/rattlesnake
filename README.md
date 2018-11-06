`bundle_lister.py` is a Python (3.6.0) web scraper that clones the clr-bundles directory, https://github.com/clearlinux/clr-bundles, parses content in bundles directory and packages file,
and then uses Jinja2 to output a file: bundles.html.txt. This ``.txt`` file is a table that appears in a webpage.

`bundle_lister.py` will be invoked in a bash script upon daily builds of the website. `bundle_lister.py` automates 
documentation so that it shows current bundles and packages per latest updates to the clr-bundles GitHub repository.  `bundle_lister.py` will be invoked, via a Makefile, so that it create the new output file upon each new build of the website. 

See `requirements.txt` for package dependencies necessary for this application.

Python==3.6.0

To run `bundle_lister.py` in the terminal, enter: `python bundle_lister.py`.

Note, you must create a directory called `cloned_repo` in order for this code to work.

Note: A successful build will produce a file named `bundles.html.txt` showing a table of current bundles and pundles (packages) alphabetized, and showing a time and date stamp (UTC) in the upper right corner of table. 
