#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


def sestej(x, y):
   return x + y

def odstej(x, y):
   return x - y

def mnozi(x, y):
   return x * y

def deli(x, y):
   return x / y


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("calc.html")
    def post(self):
        prvoSt = self.request.get("prvoStVnos")
        drugoSt = self.request.get("drugoStVnos")
        operator = self.request.get("operacijaVnos")
        prvoSt = prvoSt.strip(' ')
        drugoSt = drugoSt.strip(' ')
        prvoSt = float(prvoSt)
        drugoSt = float(drugoSt)
        if operator == "+":
            zapis = sestej(prvoSt, drugoSt)
        elif operator == "-":
            zapis = odstej(prvoSt, drugoSt)
        elif operator == "*":
            zapis = mnozi(prvoSt, drugoSt)
        elif operator == "/":
            zapis = deli(prvoSt, drugoSt)
        else:
            zapis = "Napaka!"

        podatki = {"rezultat":zapis}
        return self.render_template("calc.html", podatki)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)