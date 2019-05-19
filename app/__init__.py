from flask import Flask

app = Flask (__name__)
app.jinja_env.line_statement_prefix = '#'

from app import routes
