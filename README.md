Overview
========

Command line tool for preparing summary of products.

Installation
============

```bash
$ python setup.py install
```

Or

```bash
$ pip install -r requirements.txt
```

How to run
============


```bash
$ scl --help
Usage: scl [OPTIONS] URL

  Fetch provided URL and parse webpage for products. Tool provides summary
  of parsed products and total price of all found products.

  Usage example:

  scl http://page.com/products.html

Options:
  --help  Show this message and exit.
```


Running unit tests
==================

```bash
$ tox
```
