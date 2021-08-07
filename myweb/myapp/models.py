from django.db import models

# Create your models here.
class student(models.Model):
    '''自定义Stu表对应的Model类'''
    #定义属性：默认主键自增id字段可不写
    id = models.AutoField(primary_key=True)
    studentno = models.CharField(max_length=16)
    score = models.FloatField()
    # 定义默认输出格式
    def __str__(self):
        return "%d:%s:%d"%(self.id ,self.studentno,self.score)

    # 自定义对应的表名，默认表名：myapp_stu
    class Meta:
        db_table="result"
        verbose_name = '浏览学生信息'
        verbose_name_plural = '学生信息管理'


