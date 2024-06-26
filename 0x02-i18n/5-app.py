#!/usr/bin/env python3

""" Set up python flask application """

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz


app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale():
    """ Get the locale language """

    if 'locale' in request.args:
        requested_locale = request.args.get('locale')
        if requested_locale in app.config['LANGUAGES']:
            return requested_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id):
    """ Gets user id """
    return users.get(user_id)


@app.before_request
def before_request():
    """ display before request """
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@app.route('/')
def index():
    """ index html """
    if g.user:
        welcome_message = _("You are logged in as %(username)s.") \
            % {'username': g.user['name']}
    else:
        welcome_message = _("You are not logged in.")

    current_time = get_current_time()
    current_time_formatted = format_time(current_time)

    return render_template('index.html', welcome_message=welcome_message,
    current_time=current_time_formatted)

def get_current_time():
    """  Get the current time in the inferred time zone """
    inferred_timezone = pytz.timezone(get_timezone())
    return datetime.datetime.now(inferred_timezone)

def format_time(time):
    """ Format the time according to the default format """
    return time.strftime("%b %d, %Y, %I:%M:%S %p")

if __name__ == '__main__':
    app.run(debug=True)
