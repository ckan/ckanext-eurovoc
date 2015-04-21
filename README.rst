.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/ckan/ckanext-eurovoc.svg?branch=master
    :target: https://travis-ci.org/ckan/ckanext-eurovoc

.. image:: https://coveralls.io/repos/ckan/ckanext-eurovoc/badge.png?branch=master
  :target: https://coveralls.io/r/ckan/ckanext-eurovoc?branch=master

=============
ckanext-eurovoc
=============

Add top-level Eurovoc categories to the dataset schema.


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


-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.eurovoc --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-eurovoc on PyPI
---------------------------------

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


----------------------------------------
Releasing a New Version of ckanext-eurovoc
----------------------------------------

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
