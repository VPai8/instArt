from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{ self.user.username } Profile'

    # def save(self, *args, **kwargs):

    #     super().save()
    #     maxSize = (100, 100)
    #     try:

    #         # shrink, but maintain aspect ratio
    #         image = Image.open(self.image.path)
    #         image.thumbnail(maxSize)

    #         # fill out to exactly maxSize (square image)
    #         # use white for empty space
    #         background = Image.new("RGB", maxSize, (255, 255, 255))
    #         background.paste(
    #             image, ((maxSize[0] - image.size[0]) // 2, (maxSize[1] - image.size[1]) // 2))

    #         background.save(self.image.path)

    #     except Exception as e:

    #         print("Error resizing image: %s" % e)
