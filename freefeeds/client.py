import urllib.parse

import requests

from freefeeds.models import User, Post


class Client:
    app_key = None

    HOME_URL = "https://freefeed.net/v2/timelines/home"
    POST_URL = "https://freefeed.net/v2/posts/%s?maxComments=all"
    ME_URL = "https://freefeed.net/v1/users/me"
    
    def __init__(self, app_key):
        if not app_key:
            raise RuntimeError("App key is invalid")
        self.app_key = app_key
        
    @staticmethod
    def from_request(request):
        return Client(request.META["AUTHORIZATION"].replace("Bearer ", ""))
        
    def get_headers(self):
        return {
          "Authorization": "Bearer %s" % self.app_key
        }
    
    def request(self, url):
        result = requests.get(url, headers=self.get_headers()).json()
        return result
    
    def get_me(self):
        return User.from_feed_json(self.request(self.ME_URL)["users"])

    def get_home(self, limit=120, max_id=None, since_id=None):
        if max_id is not None:
            max_created_at = Post.objects.get(pk=max_id).created_at
        else:
            max_created_at = None
    
        if since_id is not None:
            min_created_at = Post.objects.get(pk=since_id).created_at
        else:
            min_created_at = None
    
        params = {
            "sort": "created",
            "limit": limit,
        }
        if max_created_at:
            params["created-before"] = max_created_at
        if min_created_at:
            params["created-after"] = min_created_at
        ff_data = self.request(self.HOME_URL + "?" % urllib.parse.urlencode(params)).json()
        posts = [Post.from_feed_json(p, ff_data["users"], ff_data["attachments"]) for p in ff_data["posts"]]
        
        return posts
    
    def get_post(self):
        ff_data = self.request(self.POST_URL).json()
        post = Post.from_feed_json(ff_data["posts"], ff_data["users"], ff_data["attachments"])
        
        comments = [Post.from_feed_comment_json(post, c, ff_data["users"]) for c in ff_data["comments"]]
        return [post] + comments
    
    def get_notifications(self):
        # TODO
        return []
    
    def get_user_timeline(self, md_id):
        # TODO
        return []