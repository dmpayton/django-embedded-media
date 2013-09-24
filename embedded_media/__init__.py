__author__ = 'Derek Payton <derek.payton@gmail.com>'
__copyright__ = 'Copyright (c) Derek Payton'
__description__ = 'Render inline CSS and JS in Django forms media.'
__version__ = '0.1.0'
__license__ = 'MIT License'

try:
    import django
except ImportError:
    # Django not importable, we're probably pip installing
    pass
else:
    from .media import CSS, JS
