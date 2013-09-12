=====================
django-embedded-media
=====================

.. image:: https://travis-ci.org/dmpayton/django-embedded-media.png
    :target: https://travis-ci.org/dmpayton/django-embedded-media

:Author: `Derek Payton`_
:Version: 0.0.1
:License: `MIT`_

Ever run into a situation where it would just be *so incredibly handy* to be
able to put inline CSS or JS in your form to be rendered directly on the page?

This lets you do that.

It all started with ticket `#13978`_, which I championed for a while. However,
I no longer think this is a good feature to have in Django. After using the
`#13978`_ patch for a while, I've come to realize that it's just too damn easy
to rely on it too much. No one wants a two-dozen line string of jQueryfied
JS in the middle of their form class.

However, if you've got the need for spee^H^H^H^Hembedded media -- and you think
you're disciplined enough to not start writing all your CSS and JS as strings
in your .py files -- then django-embedded-media makes it easier.

Usage
=====

There's no special configuration needed. It's a Django app, technically, but
you don't need to put it into INSTALLED_APPS. Just install the package and
start embedding your styles and scripts.

Works on forms::

    >>> from django import forms
    >>> import embedded_media as emb
    >>>
    >>> class MyForm(forms.Form):
    ...     class Media:
    ...         css = {'all': (emb.CSS('.mywidget { display: none; }'),)}
    ...         js = (emb.JS('init_mywidget();'),)

    >>> print MyForm.media
    <style type="text/css" media="all">.mywidget { display: none; }</style>
    <script type="text/javascript">init_mywidget();</script>
    >>>

Works on form widgets::

    >>> from django import forms
    >>> import embedded_media as emb
    >>>
    >>> class MyWidget(forms.TextInput):
    ...     class Media:
    ...         css = {'all': (emb.CSS('.mywidget { display: none; }'),)}
    ...         js = (
    ...             'whizbang.js',
    ...             emb.JS('init_mywidget();'),
    ...         )

    >>> print MyWidget().media
    <style type="text/css" media="all" >.mywidget { display: none; }</style>
    <script type="text/javascript" src="/static/whizbang.js"></script>
    <script type="text/javascript">init_mywidget();</script>
    >>>

Works as a dynamic media property::

    >>> from django import forms
    >>> import embedded_media as emb
    >>>
    >>> class MyForm(forms.Form):
    ...     def _media(self):
    ...         return Media(
    ...             css={'all': (emb.CSS('.mywidget { display: none; }'),)},
    ...             js=(emb.JS('init_mywidget();'),)
    ...         )
    ...     media = property(_media)

    >>> print MyForm().media
    <style type="text/css" media="all">.mywidget { display: none; }</style>
    <script type="text/javascript">init_mywidget();</script>
    >>>

Testing
=======

The tests require `Django`_, `coverage`_, and `pep8`_, which are conveniently
listed in requirements.txt::

    $ pip install -r requirements.txt
    $ python setup.py test

.. _Derek Payton: http://dmpayton.com/
.. _MIT: https://github.com/dmpayton/django-embedded-media/blob/master/LICENSE
.. _#13978: https://code.djangoproject.com/ticket/13978
.. _Django: https://crate.io/packages/Django/
.. _coverage: https://crate.io/packages/coverage/
.. _pep8: https://crate.io/packages/pep8/
