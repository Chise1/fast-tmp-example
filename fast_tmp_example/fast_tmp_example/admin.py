from fast_tmp_example.models import Author, Book, FieldTesting
from fast_tmp.site import ModelAdmin


class FieldTestingModel(ModelAdmin):
    model = FieldTesting
    list_display = (
        "name",
        "age",
        "married",
        "degree",
        "created_time",
        "birthday",
        "config",
        "max_time_length",
    )
    inline = (
        "name",
        "married",
        "birthday",
        "config",
    )
    create_fields = (
        "name",
        "age",
        "desc",
        "married",
        "degree",
        "gender",
        "created_time",
        "birthday",
        "config",
    )


class BookModel(ModelAdmin):
    model = Book
    list_display = ("name", "author", "rating", "cover")
    create_fields = ("name", "author", "rating", "cover")
    update_fields = ("name", "author", "cover")
    filters = ("name__contains",)

class AuthorModel(ModelAdmin):
    model = Author
    list_display = ("name",)
    create_fields = ("name",)
    inline = ("name",)
    update_fields = ("name",)
