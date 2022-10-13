import os

from starlette.staticfiles import StaticFiles

os.environ.setdefault("FASTAPI_SETTINGS_MODULE", "fast_tmp_example.settings")  # 请勿在此配置前面加 import
from fast_tmp.conf import settings
from fast_tmp_example.admin import AuthorModel, FieldTestingModel, BookModel
from tortoise.contrib.fastapi import register_tortoise
from fast_tmp.site import register_model_site
from fast_tmp.factory import create_app

app = create_app()
app.title = "fast_tmp_example"

register_tortoise(app, config=settings.TORTOISE_ORM, generate_schemas=True)
register_model_site({"example": [AuthorModel(), FieldTestingModel(), BookModel()]})
if settings.DEBUG:
    from fast_tmp.admin.register import register_static_service

    register_static_service(app)

if __name__ == "__main__":
    import uvicorn  # type:ignore

    uvicorn.run(app, debug=True, port=8000, lifespan="on")
