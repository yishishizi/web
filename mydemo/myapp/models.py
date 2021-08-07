from django.db import models

# Create your models here.
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
class Images(models.Model):
    img = models.ImageField(upload_to='static/pictures/')  # upload_to='static/pictures/'是指定图片存储的文件夹名称，上传文件之后会自动创建
    img_name = models.CharField(max_length=32)
    create_time = models.DateTimeField(auto_now_add=True)
>>>>>>> d984aa5 (second commit)
>>>>>>> 5548d7a (second commit)
