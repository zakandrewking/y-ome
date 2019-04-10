A y-ome is a collection of genes in an organism that lack experimental evidence
of function. This repository contains the software and analysis related to this
publication on the y-ome of _Escherichia coli_:

Sankha Ghatak, Zachary A King, Anand Sastry, Bernhard O Palsson, *The y-ome 
defines the 35% of Escherichia coli genes that lack experimental evidence of 
function*, Nucleic Acids Research, Volume 47, Issue 5, 18 March 2019, Pages 
2446–2454, https://doi.org/10.1093/nar/gkz030

# Generating a y-ome

This repository includes a SQLite database (`yome.db`), scripts for populating
the database (`bin/`), a Python package for querying the database (`yome/`), a
set of Jupyter notebooks that contain the analyses described in the manuscript
(`notebooks`), data files (`data/`), and a set of data source files
(`sources/`).

Within each source folder in `sources/`, there is a `load` script and a set of
data files. These `load` scripts are run sequentially (as defined in
`bin/load-db`) to populate the database with source-specific annotations, then
the script `bin/load-yome` generates the final y-ome gene list. The particular
rules for identifying and assessing annotations from the data sources are
described in comments within these files and also within the Methods section of
the manuscript.

When the database loads successfully, `bin/load-db` updates the following data
files in the `data/` directory:

*data/yome-genes.tsv* - A tab-separated text file containing all genes from this
analysis, their locus tags, primary name(s), and whether they are in the
"y-ome", "well-annotated", or "excluded" category.

*data/features.tsv.gz* - A tab-separated text file containing all features
extracted from the five knowledge bases. Each line contains a gene locus tag,
the knowledge base name, the gene primary name(s), the feature type for that
knowledge base, and the feature itself extracted as text.

*data/no-information.tsv* - A tab-separated text file containing a list of genes
for which no information could be found in the five knowledge bases, with locus
tags and EcoCyc primary names.

*data/common-words.tsv* - The most common words found in knowledge bases
features for y-ome genes. The counts indicate the number of unique y-ome genes
for which each phrase appears. Similar words are grouped into sets.

*data/yome-transporters.tsv* - A list of y-ome genes with indication in the knowledge
bases that they might be transporters.

# Run the workflow in Binder

Click the following link to launch the y-ome workflow in Binder. This will give
you a fully interactive Jupyter Lab session:

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/zakandrewking/y-ome/master?urlpath=lab/tree/notebooks)

# View annotation and features for a y-ome gene

When you run the Binder server, you can run the notebook called "annotation
report.ipynb" to quickly generate an overview of all the annotations for a given
gene in the database. Just follow the instructions in the notebook.

# Installation

The y-ome workflow includes a Python package that interacts with a SQLite
database. If you want to use the packaged SQLite file (`yome.db`), be sure to
install the `yome` package in `develop` mode:

```
pip install -e .
```

The `bin/load-db` script can be used to reload the database from the data in the
`sources` directory.

# EcoCyc data

EcoCyc data was downloaded using this tool:

https://github.com/zakandrewking/scrape_ecocyc
