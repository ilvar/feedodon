import urllib.parse

import requests

from freefeeds.models import User, Post, Attachment


class Client:
    app_key = None

    HOME_URL = "https://freefeed.net/v2/timelines/home"
    USER_FEED_URL = "https://freefeed.net/v2/timelines/%s"
    POSTS_URL = "https://freefeed.net/v2/posts/%s?maxComments=all"

    NEW_POST_URL = "https://freefeed.net/v1/posts"
    NEW_COMMENT_URL = "https://freefeed.net/v1/comments"
    NEW_ATTACHMENT_URL = "https://freefeed.net/v1/attachments"

    ME_URL = "https://freefeed.net/v1/users/me"

    POST_LIKE_URL = "https://freefeed.net/v1/posts/%s/like"
    POST_UNLIKE_URL = "https://freefeed.net/v1/posts/%s/unlike"
    COMMENT_LIKE_URL = "https://freefeed.net/v2/comments/%s/like"
    COMMENT_UNLIKE_URL = "https://freefeed.net/v2/comments/%s/unlike"

    def __init__(self, app_key):
        if not app_key:
            raise RuntimeError("App key is invalid")
        self.app_key = app_key
        
    @staticmethod
    def from_request(request):
        return Client(request.META["HTTP_AUTHORIZATION"].replace("Bearer ", ""))
        
    def get_headers(self):
        return {
          "Authorization": "Bearer %s" % self.app_key
        }
    
    def request(self, url, method="GET", data=None, **kwargs):
        result = requests.request(method, url, headers=self.get_headers(), json=data, **kwargs).json()
        return result
    
    def get_me(self):
        return User.from_feed_json(self.request(self.ME_URL)["users"])

    def get_home(self, limit=120, max_id=None, since_id=None):
        return self.get_feed(self.HOME_URL, limit, max_id, since_id)

    def get_feed(self, url, limit=120, max_id=None, since_id=None):
        if max_id is not None and max_id != 0:
            try:
                max_created_at = Post.objects.get(pk=max_id).created_at
            except Post.DoesNotExist:
                max_created_at = None
        else:
            max_created_at = None
    
        if since_id is not None and since_id != 0:
            try:
                min_created_at = Post.objects.get(pk=since_id).created_at
            except Post.DoesNotExist:
                min_created_at = None
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
        ff_data = self.request(url + "?" + urllib.parse.urlencode(params))
        posts = [Post.from_feed_json(p, ff_data["users"], ff_data["attachments"]) for p in ff_data["posts"]]
        
        return posts
    
    def get_post(self, md_id):
        md_post = Post.objects.get(pk=md_id)
        ff_data = self.request(self.POSTS_URL % md_post.feed_id)
        post = Post.from_feed_json(ff_data["posts"], ff_data["users"], ff_data["attachments"])
        
        comments = [Post.from_feed_comment_json(post, c, ff_data["users"]) for c in ff_data["comments"]]
        return [post] + comments
    
    def get_notifications(self):
        # TODO
        return []
    
    def get_user_timeline(self, md_id, limit=120, max_id=None, since_id=None):
        md_user = User.objects.get(pk=md_id)
        return self.get_feed(self.USER_FEED_URL % md_user.username, limit, max_id, since_id)

    def get_user(self, md_id):
        md_user = User.objects.get(pk=md_id)
        return md_user

    def post_like(self, md_id):
        post = Post.objects.get(pk=md_id)
    
        if post.parent is not None:
            self.request(self.COMMENT_LIKE_URL % post.feed_id, method="POST")
            comments = self.get_post(post.parent_id)[1:]
            comment = [p for p in comments if p.id == md_id][0]
            return comment
        else:
            self.request(self.POST_LIKE_URL % post.feed_id, method="POST")
            return self.get_post(md_id)[0]

    def post_unlike(self, md_id):
        post = Post.objects.get(pk=md_id)
    
        if post.parent is not None:
            self.request(self.COMMENT_UNLIKE_URL % post.feed_id, method="POST")
        else:
            self.request(self.POST_UNLIKE_URL % post.feed_id, method="POST")
        return self.get_post(md_id)[0]

    def new_post_or_comment(self, md_data):
        reply_id = md_data.get("in_reply_to_id", None)
        if reply_id is not None:
            post = Post.objects.get(pk=reply_id)
            
            if post.parent:
                postId = post.parent.feed_id
            else:
                postId = post.feed_id
                
            feed_data = {
                "comment": {
                    "body": md_data["status"] or '.',
                    "postId": postId
                }
            }

            new_comment = self.request(self.NEW_COMMENT_URL, method="POST", data=feed_data)
            new_md_post = Post.from_feed_comment_json(post, new_comment["comments"], new_comment["users"])
        else:
            feed_data = {
                "post": {
                    "body": md_data["status"] or '.',
                    "attachments": [Attachment.objects.get(pk=aid).feed_id for aid in md_data.getlist("media_ids[]")]
                },
                "meta": {
                    "commentsDisabled": False,
                    "feeds": [self.get_me().username]
                }
            }
    
            new_post = self.request(self.NEW_POST_URL, method="POST", data=feed_data)
            new_md_post = Post.from_feed_json(new_post["posts"], new_post["users"], [])
        
        return new_md_post
    
    def new_attachment(self, md_file):
        result = self.request(self.NEW_ATTACHMENT_URL, method="POST", files={"file": md_file})
        return Attachment.from_feed_json(None, result['attachments'])