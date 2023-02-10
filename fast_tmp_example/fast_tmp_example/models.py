"""
This is the testing Models
"""
import binascii
import datetime
import os
import uuid
from enum import Enum, IntEnum

from fast_tmp.contrib.tortoise.fields import ImageField
from tortoise import fields
from tortoise.models import Model


def generate_token():
    return binascii.hexlify(os.urandom(16)).decode("ascii")


class Author(Model):
    """
    作者
    """
    name = fields.CharField(max_length=255, description="名字")
    birthday = fields.DateField(description="生日")
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return self.name


class Book(Model):
    """
    书籍
    """
    name = fields.CharField(max_length=255, description="书名")
    author: fields.ForeignKeyRelation[Author] = fields.ForeignKeyField(
        "fast_tmp.Author", related_name="books", description="作者"
    )
    cover = ImageField(description="封面")
    rating = fields.FloatField(description="价格")
    quantity = fields.IntField(default=0, description="存量")
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)
    def __str__(self):
        return self.name


class SalesInfo(Model):
    """
    销售记录
    """
    book: fields.ForeignKeyRelation[Book] = fields.ForeignKeyField(
        "fast_tmp.Book", related_name="sales_info", description="销量记录"
    )
    num = fields.IntField(description="销售数量")
    price = fields.FloatField(description="总价")
    create_time = fields.DatetimeField(auto_now_add=True, description="成交时间")

class Gender(str, Enum):
    male = "male"
    female = "female"


class Degree(IntEnum):
    unknow = 0
    bachelor = 1  # 学士
    master = 2  # 硕士
    doctor = 3  # 博士


class FieldTesting(Model):
    name = fields.CharField(max_length=32)
    age = fields.IntField()
    desc = fields.TextField()
    birthday = fields.DateField(null=True)
    money = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    height = fields.FloatField(null=True)
    married = fields.BooleanField(default=False)
    gender = fields.CharEnumField(Gender)
    degree = fields.IntEnumField(Degree, default=Degree.unknow)
    game_length = fields.BigIntField(default=0)  # 游戏时长，按秒计算
    avator = fields.BinaryField(null=True)  # 头像
    config = fields.JSONField(null=True)
    waiting_length = fields.TimeDeltaField(null=True)  # 等待时长
    max_time_length = fields.TimeField(default=datetime.time())  # 最长游戏时长
    uuid = fields.UUIDField(default=uuid.uuid4)
    level = fields.SmallIntField(default=0)
    created_time = fields.DatetimeField(auto_now_add=True, null=True)
