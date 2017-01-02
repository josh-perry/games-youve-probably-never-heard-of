# games-you've-probably-never-heard-of
A twitter bot that posts (hopefully) obscure videogames.

[Live here!](https://twitter.com/gypnho)

# Getting it to run
## Requirements
```
pip install -r requirements.txt
```

should install all prerequisites.
## secrets.py
Create a secrets.py containing your [GiantBomb API key](http://www.giantbomb.com/api/) and your [Twitter keys](https://dev.twitter.com/) like so:
```python
# GiantBomb
gb_api_key = "abc123"

# Twitter
consumer_key = "abc123"
consumer_secret = "abc123"
access_key = "abc123"
access_secret = "abc123"
```