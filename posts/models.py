from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# class PostManager(models.Manager):
#     def get_all_posts(self, user, **kwargs):
#         q = super().get_queryset()
#         folowing = Follow.objects.filter(user1=user)
#         q = q.filter(user__in=following)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='art')
    last_edit = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=60)
    desc = models.TextField()

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):

    #     super().save(*args, **kwargs)
    #     if self.image:
    #         try:
    #             # if width more than 1080px
    #             # shrink, but maintain aspect ratio
    #             image = Image.open(self.image.path)
    #             width = self.image.width
    #             height = self.image.height
    #             ar = width / height
    #             print(width, height, ar)
    #             if 0.8 <= ar <= 1.91:
    #                 if width > 1080:
    #                     img_save = image.crop(
    #                         ((width-1080)//2, 0, (width-1080)//2+1080, 1080//ar))
    #                     print(img_save.size[0], img_save.size[1])
    #                 elif width < 320:
    #                     background = Image.new(
    #                         "RGB", (320, 320//ar), (255, 255, 255))
    #                     background.paste(
    #                         image, ((maxSize[0] - image.size[0]) //
    #                                 2, (maxSize[1] - image.size[1]) // 2))
    #                     img_save = background
    #                     print(img_save.size[0], img_save.size[1])
    #             else:
    #                 img_save = image
    #             img_save.save(self.image.path)

    #         except Exception as e:

    #             print("Error resizing image: %s" % e)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    last_edit = models.DateTimeField(auto_now=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " likes " + self.post.title


class Follow(models.Model):
    # user1 follows user2
    user1 = models.ForeignKey(
        User, related_name='follower', on_delete=models.CASCADE)
    user2 = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE)

    def __str__(self):
        return self.user1.username + " follows " + self.user2.username
