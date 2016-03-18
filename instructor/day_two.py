
# coding: utf-8

# # Day 2 - Getting Data with Python
# 
# Something about automation and scripts
# 
# Something about exceptions

# #### Let's try a challenge!
# 
# Error handling - or having a computer program anticipate and respond to errors created by other functions - is a big part of programming. To give you a little more practice with this, we're going to have you team up with person sitting next to you and try challenge B in the challenges directory.

# ## Introduction to the interwebs
# 
# A vast amount of data exists on the web and is now publicly available. In this section, we give an overview of popular ways to retrieve data from the web, and walk through some important concerns and considerations. 
# 
# ![An extremely simplified model of the web](images/Client-server-model.svg.png)
# 
# The internet follows a client-server architecture, where clients (e.g. you) ask servers to do things. 
# 
# The most common way that you experience this is through a browser, where you enter a URL and a server sends your computer a page for your browser to render. Most of what you think about as the internet are stored documents (web pages) that are given out to anyone who asks.
# 
# You probably also have a program on your computer like Outlook or Thunderbird that sends emails to a server and asks it to forward them along to someone else. You may also have proprietary software that's protected by a license, and needs to connect to a license server to verify that you are an authenticated user.
# 
# Ultimately, the internet is just connecting to computers that you don't own and passing data back and forth. Because the data transfer protocol (`http`) and typical data formats (`html`) are not native to Python, we're going to leave Python just for a little bit.

# ## Intro to HTTP requests
# 
# You can view the request sent by your browser by:
# 
# 1) Opening a new tab in your browser   
# 2) Enabling developer tools (__View -> Developer -> Developer Tools in Chrome__ and __Tools -> Web Developer -> Toggle Tools in Firefox__)  
# 3) Loading or reloading a web page (etc. www.google.com)  
# 4) Navigating to the Network tab in the panel that appears at the bottom of the page.   

# ![Chrome Examine Request Example](images/chrome_request.png)

# ![Firefox Examine Request Example](images/firefox_request.png)

# These requests you send follow the HTTP protocol (Hypertext Transfer Protocol), part of which defines the information (along with the format) the server needs to receive to return the right resources. Your HTTP request contains __headers__, which contains information that the server needs to know in order to return the right information to you. 

# But we're not here to wander around the web (you probably do this a lot, all on your own). You're here because you want Python to do it for you.
# 
# In order to get web pages, we're going to use a python library called `requests`, which takes a lot of the fuss out of contacting servers. 

# In[1]:

import requests

r = requests.get("http://en.wikipedia.org/wiki/Main_Page")


# This response object contains various information about the request you sent to the server, the resources returned, and information about the response the server returned to you, among other information. These are accessible through the <i>__request__</i> attribute, the <i>__content__</i> attribute and the <i>__headers__</i> attribute respectively, which we'll each examine below.
# 

# In[2]:

type(r.request), type(r.content), type(r.headers)


# Here, we can see that __request__ is an object with a custom type, __content__ is a str value and __headers__ is an object with "dict" in its name, suggesting we can interact with it like we would with a dictionary.
# 
# The content is the actual resource returned to us - let's take a look at the content first before examining the request and response objects more carefully. (We select the first 1000 characters b/c of the display limits of Jupyter/python notebook.)

# In[3]:

from pprint import pprint
pprint(r.content[0:1000])


# 
# The content returned is written in HTML (__H__yper__T__ext __M__arkup __L__anguage), which is the default format in which web pages are returned. The content looks like gibberish at first, with little to no spacing. The reason for this is that some of the formatting rules for the document, like its hierarchical structure, are saved in text along with the text in the document. 
# 
# > note - this is called the __D__ocument __O__bject __M__odel (DOM) and is the same way that markdown and LaTeX documents are written
# 
# If you save a web page as a ".html" file, and open the file in a text editor like Notepad++ or Sublime Text, this is the same format you'll see. Opening the file in a browser (i.e. by double-clicking it) gives you the Google home page you are familiar with. 

# You can inspect the information you sent to Wikipedia long with your request

# In[4]:

r.request.headers


# Along with the additional info that Wikipedia sent back:

# In[5]:

r.headers


# But you will probably not ever need this information.
# 
# Most of what you'll be doing is sending what are called `GET` requests (this is why we typed in `requests.get` above). This is an `HTTP` protocol for asking a server to send you some stuff. We asked Wikipedia to `GET` us their main page. Things like queries (searching Wikipedia) also fall under `GET`.
# 
# From time to time, you may also want to send information to a server (we'll do this later today). These are called `POST` requests, because you are posting something to the server (and not asking for data back).
# 
# > note - From the server's perspective, the request it receives from your browser is not so different from the request received from your console (though some servers use a range of methods to determine if the request comes from a "valid" person using a browser, versus an automated program.)
# 
# To have a look at the content of the web page, we can ask for the content:

# In[6]:

r.content[:1000]


# which gives us the response in bytes, or text:

# In[7]:

r.text[:1000]


# ## Parsing HTML in Python
# 
# Trying to parse this `str` by hand is basically a nightmare. Instead, we'll use a Python library called Beautiful Soup to turn it into something that is still confusing, but less of a nightmare.

# In[8]:

from bs4 import BeautifulSoup

page = BeautifulSoup(r.content)
page


# Beautiful Soup creates a linked tree, where the root of the tree is the whole HTML document. It has children, which are all the elements of the HTML document. Each of those has children, which are any elements they have. Each element of the tree is aware of its parent and children.
# 
# You probably don't want to iterate through each child of the whole HTML document - you want a specific thing or things in it. In some cases, you want to seach for html tags. Common tages include:
# 
# 
# | tag | function |
# |------------|------------------------------------------------------------|
# | `<title>` | The title of the web page (shows up in your browser header) |
# | `<meta>` | Information about the web page that is not shown to the user | 
# | `<a>` | Links to other web pages | 
# | `<p>` | Paragraph of text |
# 
# 
# In other cases, you want to look for IDs. These are optional information added to a tag to help developers or other code on the web page know which tag is for which purpose. Unlike tags, these are not standardized, so they will change from site to site and author to author. They will look something like:
# 
# `<div id="banner" class="MyBanner">`
# 
# With the advent of CSS (__C__ascading __S__tyle __S__heets), it is also common for people to define their own HTML styling tags. So, while things like lists (`<ol>`) and tables (`<table>`, `<tr>`, and `<td>`) are in the HTML specification, it's not safe to assume they'll be used when you expect.
# 
# As a general strategy, when web scraping, you should have the page you want to scrape open in a browser with either the Developer Tools window open, or the HTML source displayed.
# 
# We can pull out elements by tag with:

# In[9]:

page.p


# This is grabbing the paragraph tag from the page. If we want the first link from the first paragraph, we can try:

# In[10]:

page.p.a


# But what if we want all the links? We are going to use a method of bs4's elements called `find_all`.

# In[11]:

page.p.findAll('a')


# What if you want all the elements in that paragraph, and not just the links? bs4 has an iterator for children:

# In[12]:

for element in page.p.children:
    print(element)


# HTML elements can be nested, but children only iterates at one level below the element. If you want everything, you can iterate with `descendants`

# In[13]:

for element in page.p.descendants:
    print(element)


# This splits out formatting tags that we *probably* don't care about, like bold-faced text, and so we probably won't use it again.
# 
# In reality, you won't be inspecting things yourself, so you'll want to get in the habit of using your knowledge from day 2 about looping and control structures to make decisions for you. For example, what if we wanted to look at every link in the page, then print it's neighbor but only if the link is not to a media file? We could do something like:

# In[14]:

for link in page.find_all('a'):
    if link.attrs.get('class') != 'mw-redirect':
        print(link.find_next())


# #### Time for a challenge!
# 
# To make sure that everyone is on the same page (and to give you a little more practice dealing with HTML), let's partner up with the person next to you and try challenge A, on using html, in the challenges directory.

# # Creating data with web APIs
# 
# Most people who think they want to do web scraping actually want to pull data down from site-supplied APIs. Using an API is better in almost every way, and really the only reason to scrape data is if:
# 
# 1. The website was constructed in the 90s and does not have an API; or,
# 2. You are doing something illegal
# 
# If [LiveJournal has an API](http://dev.livejournal.com/), the website you are interested in probably does too.
# 
# ## What is an API?
# 
# **API** is shorthand for **A**pplication **P**rogramming **I**nterface, which is in turn computer-ese for a middleman.
# 
# Think about it this way. You have a bunch of things on your computer that you want other people to be able to look at. Some of them are static documents, some of them call programs in real time, and some of them are programs themselves.
# 
# #### Solution 1
# 
# You publish login credentials on the internet, and let anyone log into your computer
# 
# Problems:
# 
# 1. People will need to know how each document and program works to be able to access their data
# 
# 2. You don't want the world looking at your browser history
# 
# #### Solution 2
# 
# You paste everything into HTML and publish it on the internet
# 
# Problems:
# 
# 1. This can be information overload
# 
# 2. Making things dynamic can be tricky
# 
# #### Solution 3
# 
# You create a set of methods to act as an intermediary between the people you want to help and the things you want them to have access to.
# 
# Why this is the best solution:
# 
# 1. People only access what you want them to have, in the way that you want them to have it
# 
# 2. People use one language to get the things they want
# 
# Why this is still not Panglossian:
# 
# 1. You will have to explain to people how to use your middleman
# 

# ## Twitter's API
# 
# Twitter has an API - mostly written for third-party apps - that is comparatively straightforward and gives you access to _nearly_ all of the information that Twitter has about its users, including:
# 
# 1. User histories
# 
# 2. User (and tweet) location
# 
# 3. User language
# 
# 4. Tweet popularity
# 
# 5. Tweet spread
# 
# 6. Conversation chains
# 
# Also, Twitter returns data to you in json, or **J**ava **S**cript **O**bject **N**otation. This is a very common format for passing data around http connections for browsers and servers, so many APIs return it as a datatype as well (instead of using something like xml or plain text).
# 
# Luckily, json converts into native Python data structures. Specifically, every json object you get from Twitter will be a combination of nested `dicts` and `lists`, which you learned about yesterday. This makes Twitter a lot easier to manipulate in Python than html objects, for example.
# 
# Here's what a tweet looks like:

# In[15]:

import json

with open('../data/02_tweet.json','r') as f:
    a_tweet = json.loads(f.read())


# We can take a quick look at the structure by pretty printing it:

# In[16]:

from pprint import pprint

pprint(a_tweet)


# #### Time for a challenge!
# 
# Let's see how much you remember about lists and dicts from yesterday. Go into the challenges directory and try your hand at `02_scraping/C_json.py`.

# ## Authentication
# 
# Twitter controls access to their servers via a process of authentication and authorization. Authentication is how you let Twitter know who you are, in a way that is very hard to fake. Authorization is how the account owner (which will usually be yourself unless you are writing a Twitter app) controls what you are allowed to do in Twitter using their account. In Twitter, different levels of authorization require different levels of authentication. 
# 
# Because we want to be able to interact with everything, we'll need the highest level of authorization and the strictest level of authentication. In Twitter, this means that we need two sets of ID's (called keys or tokens) and passwords (called secrets):
# 
# * consumer_key
# * consumer_secret
# * access_token_key
# * access_token_secret
# 
# We'll provide some for you to use, but if you want to get your own you need to create an account on Twitter with a verified phone number. Then, while signed in to your Twitter account, go to: https://apps.twitter.com/. Follow the prompts to generate your keys and access tokens. Note that getting the second ID/password pair requires that you manually set the authorization level of your app.
# 
# We've stored our credentials in a separate file, which is smart. However, we have uploaded it to Github so that you have them too, which is not smart. 
# 
# **You should NEVER NEVER NEVER do this in real life.**
# 
# We've stored it in YAML format, because it is more human-readible than JSON is. However, once it's inside Python, these data structures behave the same way.

# In[17]:

import yaml

with open('../etc/creds.yml', 'r') as f:
    creds = yaml.load(f)


# We're going to load these credentials into a requests module specifically designed for handling the flavor of authentication management that Twitter uses.

# In[18]:

from requests_oauthlib import OAuth1Session

twitter = OAuth1Session(**creds)


# That `**` syntax we just used is called a "double splat" and is a python convenience function for converting the key-value pairs of a dictionary into keyword-argument pairs to pass to a function.

# ## Accessing the API

# Access to Twitter's API is organized through URLs called "endpoints". An endpoint is the location at which you can submit a request for Twitter to do something for you.
# 
# For example, the "endpoint" to search for specific kinds of tweets is at:
# 
# ```
# https://api.twitter.com/1.1/search/tweets.json
# ```
# 
# whereas posting new tweets is at:
# 
# ```
# https://api.twitter.com/1.1/statuses/update.json
# ```
# 
# For more information on the REST APIs, end points, and terms, check out: https://dev.twitter.com/rest/public. For the Streaming APIs: https://dev.twitter.com/streaming/overview.
# 
# All APIs on Twitter are "rate-limited" - this means that you are only allowed to ask a set number of questions per unit time (to keep their servers from being overloaded). This rate varies by endpoint and authorization, so be sure to check their developer site for the action you are trying to take.
# 
# For example, at the lowest level of authorization (Twitter calls this `application only`), you are allowed to make 450 search requests per 15 minute window, or about one every two seconds. At the highest level of authorization (Twitter calls this `user`) you can submit 180 requests every 15 minutes, or only about once every five seconds.
# 
# > side note - Google search is the worst rate-limiting I've ever seen, with an allowance of one hundred requests per day, or about once every *nine hundred seconds*
# 
# Let's try a couple of simple API queries. We're going to specify query parameters with `param`.

# In[19]:

search = "https://api.twitter.com/1.1/search/tweets.json"

r = twitter.get(search, params={'q' : 'technology'})


# This has returned an http response object, which contains data like whether or not the request succeeded:

# In[20]:

r.ok


# You can also get the http response code, and the reason why Twitter sent you that code (these are all super important for controlling the flow of your program).

# In[21]:

r.status_code, r.reason


# The data that we asked Twitter to send us in r.content

# In[22]:

r.content


# But that's not helpful. We can extract it in python's representation of json with the `json` method:

# In[23]:

r.json()


# This has some helpful metadata about our request, like a url where we can get the next batch of results from Twitter for the same query:

# In[24]:

data = r.json()
data['search_metadata']


# The tweets that we want are under the key "statuses"

# In[25]:

statuses = data['statuses']
statuses[0]


# This is one tweet.
# 
# > Depending on which tweet this is, you may or may not see that Twitter automatically pulls out links and mentions and gives you their index location in the raw tweet string
# 
# Twitter gives you a whole lot of information about their users, including geographical coordinates, the device they are tweeting from, and links to their photographs.

# Twitter supports what it calls query operators, which modify the search behavior. For example, if you want to search for tweets where a particular user is mentioned, include the at-sign, `@`, followed by the username. To search for tweets sent to a particular user, use `to:username`. For tweets from a particular user, `from:username`. For hashtags, use `#hashtag`.
# 
# For a complete set of options: https://dev.twitter.com/rest/public/search.
# 
# Let's try a more complicated search:

# In[26]:

r = twitter.get(search, params={
        'q' : 'happy',
        'geocode' : '37.8734855,-122.2597169,10mi'
    })
r.ok


# In[27]:

statuses = r.json()['statuses']
statuses[0]


# If we want to store this data somewhere, we can output it as json using the json library from above. However, if you're doing a lot of these, you'll probaby want to use a database to handle everything.

# In[28]:

with open('my_tweets.json', 'w') as f:
    json.dump(statuses, f)


# To post tweets, we need to use a different endpoint:

# In[29]:

post = "https://api.twitter.com/1.1/statuses/update.json"


# And now we can pass a new tweet (remember, Twitter calls these 'statuses') as a parameter to our post request.

# In[30]:

r = twitter.post(post, params={
        'status' : "I stole Juan's Twitter credentials"
    })
r.ok


# Other (optional) parameters include things like location, and replies.

# ## Scheduling

# The real beauty of bots is that they are designed to work without interaction or oversight. Imagine a situation where you want to automatically retweet everything coming out of the D-Lab's twitter account, "@DLabAtBerkeley". You could:
# 
# 1. spend the rest of your life glued to D-Lab's twitter page and hitting refresh; or,
# 2. write a function
# 
# We're going to import a module called `time` that will pause our code, so that we don't hit Twitter's rate limit

# In[31]:

import time

def retweet():
    r = twitter.get(search, {'q':'DLabAtBerkeley'})
    if r.ok:
        statuses = r.json()['statuses']
        for update in statuses:
            username = item['user']['screen_name']
            parameters = {'status':'HOORAY! @' + username}
            r = twitter.post(post, parameters)
            print(r.status_code, r.reason)
            time.sleep(5)


# But you are a human that needs to eat, sleep, and be social with other humans. Luckily, Linux systems have a time-based daemon called `cron` that will run scripts like this *for you*. 
# 
# > People on windows and macs will not be able to run this. That's okay.
# 
# The way that `cron` works is it reads in files where each line has a time followed by a job (these are called cronjobs). You can edit your crontab by typing `crontab -e` into a terminal.
# 
# They looks like this:

# In[32]:

with open('../etc/crontab_example', 'r') as f:
    print(f.read())


# This is telling `cron` to print that statement to a file called "dumblog" at 8am every Monday.
# 
# It's generally frowned upon to enter jobs through crontabs because they are hard to modify without breaking them. The better solution is to put your timed command into a file and copy the file into `/etc/cron.d/`. These files look like this:

# In[33]:

with open('../etc/crond_example', 'r') as f:
    print(f.read())


# At this point, you might be a little upset that you can't do this on your laptop, but the truth is you don't really want to run daemons and cronjobs on your laptop, which goes to sleep and runs out of batteries. This is what servers are for (like AWS).

# ## Now it is time for you to make your own twitter bot!
# 
# To get you started, we've put a template in the `scripts` folder. Try it out, but be generous with your `time.sleep()` calls as the whole class is sharing this account.
# 
# If you have tried to run this, or some of the earlier code in this notebook, you have probably encountered some of Twitter's error codes. Here are the most common, and why you are triggering them.
# 
# 1. `400 = bad request` - This means the API (middleman) doesn't like how you formatted your request. Check the API documentation to make sure you are doing things correctly.
# 
# 2. `401 = unauthorized` - This either means you entered your auth codes incorrectly, or those auth codes don't have permission to do what you're trying to do. It takes Twitter a while to assign posting rights to your auth tokens after you've given them your phone number. If you have just done this, wait five minutes, then try again.
# 
# 3. `403 = forbidden` - Twitter won't let you post what you are trying to post, most likely because you are trying to post the same tweet twice in a row within a few minutes of each other. Try changing your status update. If that doesn't fix it, then you are either:
# 
#     A. Hitting Twitter's daily posting limit. They don't say what this is.
#         
#     B. Trying to follow too many people, rapidly following and unfollowing the same person, or are otherwise making Twitter think you are a spambot
# 
# 4. `429 = too many requests` - This means that you have exceeded Twitter's rate limit for whatever it is you are trying to do. Increase your  `time.sleep()`  value.

# ## Considerate robots and legality 
# 
# __Typically, in starting a new web scraping project, you'll want to follow these steps:__  
# 1) Find the websites' robots.txt and do not access those pages through your bot  
# 2) Make sure your bot does not make too many requests in a specific period (etc. by using Python's sleep.wait function)   
# 3) Look up the website's term of use or terms of service. 
# 
# We'll discuss each of these briefly.
# 
# ### What data owners care about
# 
# __Data owners are concerned with:__  
# 1) Keeping their website up  
# 2) Protecting the commercial value of their data   
# 
# Their policies and responses differ with respect to these two areas. You'll need to do some research to determine what is appropriate with regards to your research. 
# 
# #### 1) Keeping their website up
# Most commercial websites have strategies to throttle or block IPs that make too many requests within a fixed amount of time. Because a bot can make a large number of requests in a small amount of time (etc. entering 100 different terms into Google in one second), servers are able to determine if traffic is coming from a bot or a person (among many other methods). For companies that rely on advertising, like Google or Twitter, these requests do not represent "human eyeballs" and need to be filtered out from their bill to advertisers. 
# 
# In order to keep their site up and running, companies may block your IP temporarily or permanently if they detect too many requests coming from your IP, or other signs that requests are being made by a bot instead of a person. If you systematically down a site (such as sending millions of requests to an official government site), there is the small chance your actions may be interpreted maliciously (and regarded as hacking), with risk of prosecution. 
# 
# #### 2) Protecting the commercial value of their data
# Companies are also typically very protective of their data, especially data that ties directly into how they make money. A listings site (like Craigslist), for instance, would lose traffic if listings on its site were poached and transfered to a competitor, or if a rival company used scraping tools to derive lists of users to contact. For this reason, companies' term of use agreements are typically very restrictive of what you can do with their data. 
# 
# Different companies may have a range of responses to your scraping, depending on what you do with the data. Typically, repurposing the data for a rival application or business will trigger a strong response from the company (i.e. legal attention). Publishing any analysis or results, either in a formal academic journal or on a blog or webpage, may be of less concern, though legal attention is still possible. 
# 
# ### robots.txt: internet convention
# 
# The robots.txt file is typically located in the root folder of the site, with instructions to various services (User-agents) on what they are not allowed to scrape. 
# 
# Typically, the robots.txt file is more geared towards search engines (and their crawlers) more than anything else. 
# 
# However, companies and agencies typically will not want you to scrape any pages that they disallow search engines from accessing. Scraping these pages makes it more likely for your IP to be detected and blocked (along with other possible actions.) 
# 
# Below is an example of reddit's robots.txt file: 
# https://www.reddit.com/robots.txt
# 
# # 80legs
# User-agent: 008
# Disallow: /
# 
# User-Agent: bender
# Disallow: /my_shiny_metal_ass
# 
# User-Agent: Gort
# Disallow: /earth
# 
# User-Agent: *  
# Disallow: /*.json  
# Disallow: /*.json-compact  
# Disallow: /*.json-html  
# Disallow: /*.xml  
# Disallow: /*.rss  
# Disallow: /*.i  
# Disallow: /*.embed  
# Disallow: /*/comments/*?*sort=  
# Disallow: /r/*/comments/*/*/c*  
# Disallow: /comments/*/*/c*  
# Disallow: /r/*/submit  
# Disallow: /message/compose*  
# Disallow: /api   
# Disallow: /post  
# Disallow: /submit  
# Disallow: /goto  
# Disallow: /*after=  
# Disallow: /*before=  
# Disallow: /domain/*t=  
# Disallow: /login  
# Disallow: /reddits/search  
# Disallow: /search  
# Disallow: /r/*/search  
# Allow: /  
# 
# User blahblahblah provides a concise description of how to read the robots.txt file:
# https://www.reddit.com/r/learnprogramming/comments/3l1lcq/how_do_you_find_out_if_a_website_is_scrapable/
# 
# - The bot that calls itself 008 (apparently from 80legs) isn't allowed to access anything
# - bender is not allowed to visit my_shiny_metal_ass (it's a Futurama joke, the page doesn't actually exist)
# - Gort isn't allowed to visit Earth (another joke, from The Day the Earth Stood Still)
# - Other scrapers should avoid checking the API methods or "compose message" or 'search" or the "over 18?" page (because those aren't something you really want showing up in Google), but they're allowed to visit anything else.
# 
# In general, your bot will fall into the * wildcard category of what the site generally do not want bots to access. You should make sure your scraper does not access any of those pages, etc. www.reddit.com/login etc. 

# In[34]:



