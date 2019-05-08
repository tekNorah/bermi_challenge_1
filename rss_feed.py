#import gevent
#from gevent import monkey; monkey.patch_all()
import time
from datetime import datetime, timedelta

import feedparser as fp
import pytz


subscriptions = [
    'https://9gag-rss.com/api/rss/get?code=9GAGDarkHumorNoGif&format=2',
    'https://9gag-rss.com/api/rss/get?code=9GAGFresh&format=2',
    'https://9gag-rss.com/api/rss/get?code=9GAGDarkHumor&format=2',
    'https://9gag-rss.com/api/rss/get?code=9GAGAwesome&format=2']

# Date and time setup. I want only posts from "today,"
# where the day lasts until 2 AM.
utc = pytz.utc
homeTZ = pytz.timezone('US/Arizona')
dt = datetime.now(homeTZ)
if dt.hour < 2:
    dt = dt - timedelta(hours=24)
start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
start = start.astimezone(utc)


# Collect all of today's posts and put them in a list of tuples.
posts = []
sub_titles = []


def get_posts():
    for s in subscriptions:
        f = fp.parse(s, request_headers={'Cache-control': 'max-age=60'})
        try:
            blog = f['feed']['title']
        except KeyError:
            continue
        for e in f['entries']:
            try:
                when = e['published_parsed']
            except KeyError:
                when = e['updated_parsed']
            when = utc.localize(datetime.fromtimestamp(time.mktime(when)))
            if when > start:
                title = e['title']
                try:
                    body = e['content'][0]['value']
                except KeyError:
                    body = e['summary']
                link = e['link']
                posts.append((when, blog, title, link, body))

                # Sort the posts in reverse chronological order.
                posts.sort()
                posts.reverse()
    return posts

def get_single_blog(feed):
    '''Feed the all_posts path an individual blog/feed to parse and display from inside the template'''
    the_feed = fp.parse(feed, request_headers={'Cache-control': 'max-age=60'})
    single_blog_posts = the_feed['entries']
    for single_blog_post in single_blog_posts:
      try:
        when = single_blog_post['published_parsed']
      except KeyError:
        when = single_blog_post['updated_parsed']
      when = utc.localize(datetime.fromtimestamp(time.mktime(when)))
      single_blog_post['updated'] = when.astimezone(homeTZ).strftime('%b %d, %Y %I:%M %p')
    single_blog_title = the_feed['feed']['title']
    return single_blog_posts, single_blog_title


def get_subscriptions():
    '''simple method to pass the subscriptions (will improve here)'''
    sub_urls = subscriptions
    for sub in subscriptions:
        f = fp.parse(sub, request_headers={'Cache-control': 'max-age=60'})
        try:
            sub_titles.append(f['feed']['title'])
        except KeyError:
            continue
    subs = dict(zip(sub_titles, sub_urls))
    return subs

# TODO: pick the most efficient option: generate html in template or in code
def get_sorted_posts(sorted_posts):
    '''
    This method returns generated html with the days posts. Contrast to the get_single_blog method that
    generates the html inside the template.'''
    listTemplate = ''' <section>
                <h2 class="page-header no-margin-top"><a href="{3}">{2}</a></h2>
                <p>{4}</p>
            <div class="panel-footer">
                        <div class="row">
                            <div class="col-md-12">
                                <i class="fa fa-clock-o"></i> {0} <i class="fa fa-user"> </i> <a href="{3}">{1}</a>.
                            </div>
                        </div>
                    </div>
            </section>'''
    litems = []
    for p in sorted_posts:
        q = [x for x in p[1:]]
        timestamp = p[0].astimezone(homeTZ)
        q.insert(0, timestamp.strftime('%b %d, %Y %I:%M %p'))
        litems.append(listTemplate.format(*q))
    myitems = '</br>'.join(litems)
    return myitems

def nest_subs(subs):
    # convert sub dict to nested dict list and add record id
  nested_subs = []
  number = 0
  for title,url in subs.items():
  #   print(title)
    number += 1
    nested_subs.append({'id':number,'title':title,'url':url})
  return nested_subs