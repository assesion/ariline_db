from django.db import models

# Create your models here.
class Ydjl(models.Model):
    user = models.CharField(db_column='USER', max_length=25, blank=True, null=True)  # Field name made lowercase.
    xm = models.CharField(db_column='XM', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='TEL', max_length=11, blank=True, null=True)  # Field name made lowercase.
    hbbh = models.CharField(db_column='HBBH', max_length=4, blank=True, null=True)  # Field name made lowercase.
    dpsj = models.DateTimeField(db_column='DPSJ', blank=True, null=True)  # Field name made lowercase.
    sfzh = models.CharField(db_column='SFZH', max_length=255, blank=True, null=True)  # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'YDJL'



class Hb(models.Model):
    bh = models.CharField(db_column='BH', primary_key=True, max_length=255)  # Field name made lowercase.
    qd = models.CharField(db_column='QD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    zd = models.CharField(db_column='ZD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    qfsj = models.DateTimeField(db_column='QFSJ', blank=True, null=True)  # Field name made lowercase.
    hxbh = models.CharField(db_column='HXBH', max_length=255, blank=True, null=True)  # Field name made lowercase.
    yp = models.IntegerField(db_column='YP',  blank=True, null=True)  # Field name made lowercase.
    zp = models.CharField(db_column='ZP', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ddsj = models.DateTimeField(db_column='DDSJ', blank=True, null=True)  # Field name made lowercase.
    pj = models.CharField(db_column='PJ', max_length=25, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HB'


class Hx(models.Model):
    hxbh = models.CharField(db_column='HXBH', primary_key=True, max_length=4)  # Field name made lowercase.
    zd = models.CharField(db_column='ZD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    qd = models.CharField(db_column='QD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    fjxh = models.CharField(db_column='FJXH', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HX'


class User(models.Model):
    user = models.CharField(db_column='USER', primary_key=True, max_length=255)  # Field name made lowercase.
    passwd = models.CharField(db_column='PASSWD', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='TEL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mail = models.CharField(db_column='MAIL', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lx = models.CharField(db_column='LX', max_length=255, blank=True, null=True)  # Field name made lowercase.


    class Meta:
        managed = False
        db_table = 'USER'
