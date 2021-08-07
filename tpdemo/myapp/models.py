from django.db import models

# Create your models here.
class District(models.Model):
    name=models.CharField(max_length=255)
    upid=models.IntegerField()
    # 定义默认输出格式
    def __str__(self):
        return "%d:%s"%(self.upid ,self.name)

    class Meta:
        db_table="district"

