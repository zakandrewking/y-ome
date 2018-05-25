# Run the workflow in Binder

Click the following link to launch the Y-ome workflow in Binder. This will give
you a fully interactive Jupyter Lab session:

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/zakandrewking/y-ome/master?urlpath=lab/tree/notebooks)

# Installation

The Y-ome workflow includes a Python package that interacts with a sqlite
database. If you want to use the packaged sqlite file, be sure to install the
`yome` package in `develop` mode:

```
pip install -e .
```

The `bin/load_db` script can be used to reload the database from the data in the
`sources` directory.

The `notebooks` directory contains a set of Jupyter notebooks that query the
sqlite database to generate figures and Y-ome summaries.

# EcoCyc data

EcoCyc data was downloaded using this tool:

https://github.com/zakandrewking/scrape_ecocyc
