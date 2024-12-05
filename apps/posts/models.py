from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel

User = get_user_model()


class Post(TimeStampedModel):
    author = models.ForeignKey(
        User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(verbose_name=_("Title"), max_length=250)
    slug = models.SlugField(unique=True)
    body = models.TextField(verbose_name=_("Post"))
    banner_image = CloudinaryField(verbose_name=_("Banner Image"), blank=True, null=True)
    bookmarked_by = models.ManyToManyField(
        User, related_name="bookmarked_posts", blank=True
    )
    upvotes = models.PositiveIntegerField(default=0, verbose_name=_("Upvotes"))
    upvoted_by = models.ManyToManyField(User, related_name="upvoted_posts", blank=True)
    downvotes = models.PositiveIntegerField(default=0, verbose_name=_("Downvotes"))
    downvoted_by = models.ManyToManyField(
        User, related_name="downvoted_posts", blank=True
    )

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_random_string(length=6)
        super().save(*args, **kwargs)


class Image(models.Model):
    image = CloudinaryField(verbose_name=_("Image"), null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")

    def __str__(self) -> str:
        return f"{self.image}"

    def author(self):
        return self.post.author
