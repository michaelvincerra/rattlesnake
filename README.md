`bundle_lister.py` is a Python (3.6.0) web scraper that clones the clr-bundles directory, https://github.com/clearlinux/clr-bundles, parses content all bundles in the clr-bundles directory and the `packages-descriptions` file, and then uses Jinja2 to output the result of the analysis to: bundles.html.txt. This ``.txt`` file is referenced inside of a `bundles.rst` file, whose title is `Available bundles`, that currently appears at: https://clearlinux.org/documentation/clear-linux/reference/bundles.

`bundle_lister.py` automates documentation so it shows current bundles and packages per latest updates to the clr-bundles GitHub repository.  `bundle_lister.py` will be invoked, via a in a bash script in the `source/Makefile`. In this way, `bundle_lister.py` will automatically create newly scraped and parsed data from the clr-bundles directory, upon each build of the website, and output an accurate, up-to-date table that shows all bundles and packages for interested Linux developers and admins. 

See `requirements.txt` for dependencies necessary to run this application.

Python==3.6.0

To run `bundle_lister.py` in the terminal, enter: `python bundle_lister.py`.

Note, the `cloned_repo` directory must remain in the parent directory in order for this code to work.

Note: A successful build will produce a file named `bundles.html.txt` showing a table of current bundles and pundles (packages) alphabetized, and showing a time and date stamp (UTC) in the upper right corner of table. 

`~$~`
