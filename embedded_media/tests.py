import embedded_media as emb
from django.forms import Form, CharField, TextInput, Media
from django.test import TestCase


class EmbeddedMediaTest(TestCase):
    def test_css(self):
        ## CSS rendering
        css = emb.CSS('.mywidget { display: none; }')
        self.assertHTMLEqual(css.render('all'),
            '<style type="text/css" media="all">.mywidget { display: none; }</style>')

    def test_js(self):
        ## JS rendering
        js = emb.JS('init_mywidget();')
        self.assertHTMLEqual(js.render(),
            '<script type="text/javascript">init_mywidget();</script>')

    def test_media(self):
        ## Embedded JavaScript and CSS
        class MyWidget(TextInput):
            class Media:
                css = {'all': (emb.CSS('.mywidget { display: none; }'),)}
                js = (emb.JS('init_mywidget();'),)

        w = MyWidget()
        self.assertHTMLEqual(str(w.media['css']),
            '<style type="text/css" media="all">.mywidget { display: none; }</style>')
        self.assertHTMLEqual(str(w.media['js']),
            '<script type="text/javascript">init_mywidget();</script>')

    def test_property(self):
        ## Embedded JavaScript and CSS as a media property
        class MyWidget(TextInput):
            def _media(self):
                return Media(
                    css={'all': (emb.CSS('.mywidget { display: none; }'),)},
                    js=(emb.JS('init_mywidget();'),)
                )
            media = property(_media)

        w = MyWidget()
        self.assertHTMLEqual(str(w.media['css']),
            '<style type="text/css" media="all">.mywidget { display: none; }</style>')
        self.assertHTMLEqual(str(w.media['js']),
            '<script type="text/javascript">init_mywidget();</script>')

    def test_mutiple(self):
        ## Multiple instances of embedded media should only be rendered once
        class MyWidget(TextInput):
            def _media(self):
                return Media(
                    css={'all': (emb.CSS('.mywidget { display: none; }'),)},
                    js=(emb.JS('init_mywidget();'),)
                )
            media = property(_media)

        class MyForm(Form):
            field1 = CharField(widget=MyWidget)
            field2 = CharField(widget=MyWidget)

        f = MyForm()
        self.assertHTMLEqual(str(f.media), """
            <style type="text/css" media="all">.mywidget { display: none; }</style>
            <script type="text/javascript">init_mywidget();</script>
        """)
