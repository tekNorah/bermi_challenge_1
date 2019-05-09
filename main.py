import os

from flask import Flask, render_template, request, jsonify, abort, make_response

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from rss_feed import get_sorted_posts, get_posts, get_single_blog, get_subscriptions, nest_subs, get_all_entries

# set up base directory
basedir = os.path.abspath(os.path.dirname(__file__))

'''----------APP SETUP-------------'''
app = Flask(__name__)

# Set up Simple Cache
#cache = Cache(app,config={'CACHE_TYPE': 'simple'})

# Set secret key for csrf in WTF forms
# app.config['SECRET_KEY'] = 'kjer9034-09uei0909KW454()%(Q#)(I)(IKJWEI'

bootstrap = Bootstrap(app)

# init flask moment to add simple date/time to templates
moment = Moment(app)

@app.route('/')
def index():
    page_title = 'Today\'s Posts from all feeds'
    posts = get_posts()
    my_posts = get_sorted_posts(posts)
    return render_template('index.html', my_posts=my_posts, page_title=page_title)


@app.route('/all_posts')
def all_posts():
    '''Renders the feed sent from the /subscriptions page'''
    subs = request.args.get('sub')
    the_posts, sub_title = get_single_blog(subs)
    page_title = 'All posts from: %s' % sub_title
    return render_template('all_posts.html', the_posts=the_posts, page_title=page_title)


@app.route('/subscriptions')
def subscriptions():
    ''' Grabs the list of subscriptions and renders them to this page'''
    subs = get_subscriptions()
    page_title = 'All Subscriptions'
    return render_template('subs.html', subs=subs, page_title=page_title)

@app.route('/api')
def api():
    ''' Grabs the list of subscriptions and renders them to this page'''
    subs = nest_subs(get_subscriptions())
    print(subs)
    page_title = 'API Endpoints'
    return render_template('api.html', subs=subs, page_title=page_title)

@app.route('/api/v1.0/subscriptions', methods=['GET'])
def get_subs():
    subs = nest_subs(get_subscriptions())
    return jsonify({'subscriptions': subs})

@app.route('/api/v1.0/subscriptions/all', methods=['GET'])
def get_all_subs():
    subs = get_all_entries()
    return jsonify({'subscriptions': subs})

@app.route('/api/v1.0/subscriptions/<int:sub_id>', methods=['GET'])
def get_sub(sub_id):
    subs = nest_subs(get_subscriptions())
    sub = [sub for sub in subs if sub['id'] == sub_id]
    if len(sub) == 0:
        abort(400)
    return jsonify({'subscription': sub[0]})

@app.route('/api/v1.0/subscriptions/<int:sub_id>/entries', methods=['GET'])
def get_sub_entries(sub_id):
    subs = nest_subs(get_subscriptions())
    sub = [sub for sub in subs if sub['id'] == sub_id]
    if len(sub) == 0:
        abort(400)
    sub_entries, sub_titles = get_single_blog(sub[0]['url'])
    return jsonify({'subscription': sub[0]},{'entries': sub_entries})

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 400)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0')
