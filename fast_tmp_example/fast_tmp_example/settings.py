import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "VAO.c'hn+,)bAajOXa!hx(p^N'!N`[!`O#oRgj]FJcG*Vnkh+T.@ABQSK%xg*xZ"

DEBUG = True

TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://fast_tmp_example.sqlite3",
    },
    'apps': {
        'fast_tmp': {
            'models': ['fast_tmp.models','fast_tmp_example.models' ],  # 注册app.models
            'default_connection': 'default',
        }
    }
}
EXTRA_SCRIPT = []  # 自定义执行脚本