.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/ckan/ckanext-eurovoc.svg?branch=master
    :target: https://travis-ci.org/ckan/ckanext-eurovoc

.. image:: https://coveralls.io/repos/ckan/ckanext-eurovoc/badge.png?branch=master
  :target: https://coveralls.io/r/ckan/ckanext-eurovoc?branch=master

===============
ckanext-eurovoc
===============

Add top-level Eurovoc categories to CKAN for search and filtering.


------------
Requirements
------------

Compatible with CKAN 2.2 and 2.3.


------------
Installation
------------

.. Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-eurovoc:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-eurovoc Python package into your virtual environment::

     pip install ckanext-eurovoc

3. Add ``eurovoc`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


------------------------
Development Installation
------------------------

To install ckanext-eurovoc for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/ckan/ckanext-eurovoc.git
    cd ckanext-eurovoc
    python setup.py develop
    pip install -r dev-requirements.txt


-------------
Configuration
-------------

Adding templates, and Eurovoc category field to the dataset schema
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The Eurovoc plugin doesn't automatically change CKAN templates or add a Eurovoc
category field to your dataset schema.

If you want to add eurovoc category values to your schema, you will need to
modify the dataset schema in your own extension and add form widgets to the
appropriate templates.

You can use the example templates in ``eurovoc/templates/package/snippets`` to
add a form field for creating or editing Eurovoc category values in a dataset.

If you aren't adding your own extension, or you aren't modifying the dataset
schema, you can add the optional ``eurovoc_dataset`` plugin to
``ckan.plugins`` to integrate the Eurovoc category field into your schema and
templates.

If you are defining your own Eurovoc category field name, ensure you have set
it as the value for ``ckanext.eurovoc.category_field_name``, as mentioned
below.


ckanext.eurovoc.categories
++++++++++++++++++++++++++

The display language for Eurovoc category labels and additional solr search
terms are defined in category configuration files. These should be placed in
``eurovoc/categories/categories_*.json``, where '*' is the two-letter
country code for the language used.

The category config file to be used is defined in ckan config::

    ckanext.eurovoc.categories = categories_se.json  # sweden

If no categories file is defined, ``categories_en.json`` is used.

If the category file is changed, the solr search index will need to be rebuilt
for the changes to fully take effect::

    paster search-index rebuild


ckanext.eurovoc.category_field_name
+++++++++++++++++++++++++++++++++++

It is sometimes necessary to customise the dataset schema field name being
used to store the eurovoc category value. This can be set in the ckan config,
e.g.::

    ckanext.eurovoc.category_field_name = theme

The default value is ``eurovoc_category``.

Note: Changing the value of ``category_field_name`` will not migrate previous
values assigned to the old field name.


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.eurovoc --cover-inclusive --cover-erase --cover-tests


-----------------------------------
Registering ckanext-eurovoc on PyPI
-----------------------------------

ckanext-eurovoc should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-eurovoc. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


------------------------------------------
Releasing a New Version of ckanext-eurovoc
------------------------------------------

ckanext-eurovoc is availabe on PyPI as https://pypi.python.org/pypi/ckanext-eurovoc.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
