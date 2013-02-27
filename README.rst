Introduction
============

plomino.easynewsletter extends the Products.EasyNewsletter behavior to allow to define external suscribersource.

Usage
=====

In the Plone control panel, go to the "EasyNewsLetter Correspondance" control panel and enter:

One external source by line using the following format ::

    source_group1:/Site1/page1/agent1
    source_group2:/Site2/page2/agent2


Example of outputs 
------------------
::

	st = [{ "salutation" : "salut", "fullname" : "Davisp Pylon", "email" : "davisp@xenbox.fr"},
	      { "salutation" : "hello", "fullname" : "Joe Travis", "email" : "travis@xenbox.fr"},
	]
	return st
	
This code is an example of agent in plomino : the address to use it is /Site1/page1/agent1 and not /Site1/page1/agent1/runAgent


INSTALL
=======

Add plomino.easynewsletter to your buildout eggs.


It depends on:

    - CMFPlomino
    - Products.EasyNewsletter
    
Credits
=======

Companies
---------

|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_


Authors
-------

- Julien Marinescu davisp1 <davisp@xenbox.fr>

.. Contributors

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

