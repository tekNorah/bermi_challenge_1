# Summary
[Code Challenge](http://codefor.cash/bermi) for Bermi Back End Engineer Position via codefor.cash

# Demo
[Web UI](https://flask-rss-reader--teknorah.repl.co/)
Pages:
 - Home (index) - All of today's (Arizona time zone) entries from all subscriptions
 - Subscriptions - List of Subscriptions
 - Subscription Page - List of Entries for a Single Subscription

# API
Base URL: https://flask-rss-reader--teknorah.repl.co/api/v1.0/subscriptions
 - {Base_url} - List of Subscriptions
 - {Base_url}/all - List of All Subscriptions with their Entries
 - {Base_url}/{sub_id} - Single Subscription Information
 - {Base_url}/{sub_id}/entries - Single Subscription's Entries

# Technology
Build with Python and the following libraries
 - feedparser==5.2.1
 - Flask==1.0.2
 - pytz==2019.1
 - Flask-Bootstrap==3.3.7.1
 - Flask-Moment==0.7.0
 - Flask-Script==2.0.6
