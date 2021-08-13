import arrow
from django.db import models


class FfToMdConvertorMixin:
    @staticmethod
    def dt_from_frf(frf_ts):
        return arrow.get(int(frf_ts) / 1000).format('YYYY-MM-DDTHH:mm:ss.SSS') + "Z"

    @staticmethod
    def dt_to_md(dt):
        return arrow.get(dt).format('YYYY-MM-DDTHH:mm:ss.SSS') + "Z"


class User(models.Model, FfToMdConvertorMixin):
    feed_id = models.CharField(max_length=100, db_index=True)
    username = models.CharField(max_length=100)
    screen_name = models.CharField(max_length=100)
    avatar_url = models.URLField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    
    @staticmethod
    def from_feed_json(ff_user):
        try:
            return User.objects.get(feed_id=ff_user["id"])
        except User.DoesNotExist:
            return User.objects.create(
                feed_id = ff_user["id"],
                username = ff_user["username"],
                screen_name = ff_user["screenName"],
                avatar_url = ff_user["profilePictureMediumUrl"],
                created_at = User.dt_from_frf(ff_user["createdAt"]),
                updated_at=User.dt_from_frf(ff_user["updatedAt"]),
            )

    def to_md_json(self):
        return {
            "id": self.pk,
            "username": self.username,
            "acct": "%s" % self.username,
            "display_name": self.screen_name,
            "locked": False,
            "created_at": User.dt_to_md(self.created_at),
            "followers_count": 0,
            "following_count": 0,
            "statuses_count": 0,
            "note": "",
            "uri": "https://freefeed.net/%s" % self.username,
            "url": "https://freefeed.net/%s" % self.username,
            "avatar": self.avatar_url,
            "avatar_static": self.avatar_url,
            "header": "",
            "header_static": "",
            "emojis": [],
            "bot": False
        }

class Post(models.Model, FfToMdConvertorMixin):
    feed_id = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(null=True)

    @staticmethod
    def from_feed_json(ff_post, all_ff_users, all_ff_attachments):
        try:
            md_post = Post.objects.get(feed_id=ff_post["id"], parent__isnull=True)
        except Post.DoesNotExist:
            ff_user = [u for u in all_ff_users if u["id"] == ff_post["createdBy"]][0]
            md_user = User.from_feed_json(ff_user)
            md_post = Post.objects.create(
                feed_id=ff_post["id"],
                parent = None,
                user=md_user,
                created_at=Post.dt_from_frf(ff_post["createdAt"])
            )

        md_post.data = dict(
            body=ff_post["body"],
            likes=len(ff_post["likes"]) + ff_post["omittedLikes"],
            comments=len(ff_post["comments"]) + ff_post["omittedComments"],
            comments_disabled=ff_post["commentsDisabled"],
            updated_at=Post.dt_from_frf(ff_post["updatedAt"])
        )

        md_post.attachments = []
    
        for ff_attachment in all_ff_attachments:
            if ff_attachment["id"] in ff_post["attachments"] and ff_attachment["mediaType"] == "image":
                md_post.attachments.append(Attachment.from_feed_json(md_post, ff_attachment))
    
        return md_post

    @staticmethod
    def from_feed_comment_json(parent_post, ff_comment, all_ff_users):
        try:
            md_post = Post.objects.get(feed_id=ff_comment["id"])
        except Post.DoesNotExist:
            ff_user = [u for u in all_ff_users if u["id"] == ff_comment["createdBy"]][0]
            md_user = User.from_feed_json(ff_user)
            md_post = Post.objects.create(
                feed_id=ff_comment["id"],
                parent=parent_post,
                user=md_user,
                created_at=Post.dt_from_frf(ff_comment["createdAt"])
            )
            
        md_post.attachments = []

        md_post.data = dict(
            body=ff_comment["body"],
            likes=ff_comment.get("likes", 0),
            comments=0,
            comments_disabled=False,
            updated_at=Post.dt_from_frf(ff_comment.get("updatedAt", ff_comment["createdAt"])),
        )

        return md_post

    def get_absolute_url(self):
        if self.parent is not None:
            return "https://freefeed.net/%s/%s" % (self.parent.user.username, self.parent.feed_id)
        else:
            return "https://freefeed.net/%s/%s" % (self.user.username, self.feed_id)

    def to_md_json(self):
        return {
            "id": self.pk,
            "uri": self.get_absolute_url(),
            "url": self.get_absolute_url(),
            "account": self.user.to_md_json(),
            "content": self.data["body"],
            "created_at": Post.dt_to_md(self.created_at),
            "emojis": [],
            "replies_count": self.data["comments"],
            "reblogs_count": self.data["comments"],
            "favourites_count": self.data["likes"],
            "sensitive": False,
            "reblog": None,
            "in_reply_to_id": None,
            "spoiler_text": "",
            "visibility": "public",
            "media_attachments": [a.to_md_json() for a in self.attachments],
            "mentions": [],
            "tags": [],
            "application": {"name": "Freefeed"},
            "language": "ru", # TODO
            "pinned": False
        }
    
class Attachment(models.Model, FfToMdConvertorMixin):
    feed_id = models.CharField(max_length=100, db_index=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)

    @staticmethod
    def from_feed_json(md_post, ff_attachment):
        try:
            att = Attachment.objects.get(feed_id=ff_attachment["id"])
            if att.post is None and md_post is not None:
                att.post = md_post
                att.save()
        except Attachment.DoesNotExist:
            att = Attachment.objects.create(
                feed_id=ff_attachment["id"],
                post=md_post
            )

        att.data = dict(
            media_type=ff_attachment["mediaType"],
            url=ff_attachment["url"],
            thumbnail_url=ff_attachment["thumbnailUrl"],
            width=ff_attachment["imageSizes"]["o"]["w"],
            height=ff_attachment["imageSizes"]["o"]["h"]
        )
        return att
    
    def to_md_json(self):
        return {
            "id": self.pk,
            "type": self.data["media_type"],
            "url": self.data["url"],
            "remote_url": self.data["url"],
            "preview_url": self.data["thumbnail_url"],
            "text_url": "",
            "meta": (self.data["width"] and self.data["height"]) and{
              "width": self.data["width"],
              "height": self.data["height"]
            } or {},
            "description": ""
        }