import datetime

from fast_tmp_example.models import Author, Book, FieldTesting, SalesInfo
from fast_tmp.site import ModelAdmin

from fast_tmp.amis.formitem import DateItem
from fast_tmp.amis.forms import Form
from fast_tmp.amis.page import Page
from fast_tmp.amis.view.chart import Chart
from fast_tmp.amis.view.divider import Divider
from fast_tmp.responses import BaseRes
from fast_tmp.site import PageRouter
from starlette.requests import Request
from tortoise.transactions import in_transaction


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
    ordering = ("author",)


class AuthorModel(ModelAdmin):
    model = Author
    list_display = ("name", "birthday")
    inline = ("name",)
    create_fields = ("name", "birthday")
    update_fields = ("name", "birthday")
    ordering = ("name",)


class SalesInfoModel(ModelAdmin):
    model = SalesInfo
    list_display = ("book","num","price","create_time")
    create_fields = list_display
class SalesInfoPage(PageRouter):

    async def router(self, request: Request, prefix: str, method: str) -> BaseRes:
        if prefix == "list" and method == "GET":  # 获取请求信息
            starttime = request.query_params.get("starttime") or (
                    datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
            endtime = request.query_params.get("endtime") or (
                    datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            start_day = datetime.datetime.strptime(starttime, "%Y-%m-%d")
            end_day = datetime.datetime.strptime(endtime, "%Y-%m-%d")
            # 按照天对交易时间分类并统计每天成交数
            async with in_transaction() as conn:
                data_raw = (await conn.execute_query(
                    f'select date(create_time) as "day",count(id) from salesinfo where day>="{starttime}" and day<="{endtime}" group by day order by day'
                ))[1]
                if len(data_raw) == 0:
                    return BaseRes(data=[])

                data_s = []
                data_v = []

                day = start_day
                while day <= end_day:
                    date = day.strftime("%Y-%m-%d")
                    data_s.append(date)
                    for i in data_raw:  # 需要优化
                        if i[0] == date:
                            data_v.append(i[1])
                            break
                    else:
                        data_v.append(0)
                    day += datetime.timedelta(days=1)
                return BaseRes(data={  # 返回echarts标准数据
                    "title": {"text": "销售情况"},
                    "xAxis": {"type": "category", "data": data_s},
                    "yAxis": {"type": "value"},
                    "series": [{"data": data_v, "type": "line"}]
                })
        return BaseRes(data=[])

    async def get_app_page(self, request: Request) -> Page:
        return Page(
            # 返回页面信息，该页面的json格式为：{"status":0,"msg":"","data":{"type":"page","body":[{"type":"form","title":"过滤条件","api":"get: sales_info/extra/list?starttime=${starttime}&endtime=${endtime}","body":[{"type":"input-date","name":"starttime","label":"开始日期","value":"-8days","format":"YYYY-MM-DD","inputFormat":"YYYY-MM-DD","utc":false},{"type":"input-date","name":"endtime","label":"结束日期","value":"-1days","format":"YYYY-MM-DD","inputFormat":"YYYY-MM-DD","utc":false}],"mode":"inline","target":"chart1"},{"type":"divider"},{"type":"chart","name":"chart1","api":"get: sales_info/extra/list?starttime=${starttime}&endtime=${endtime}"}]}}
            body=[
                Form(
                    title="过滤条件",
                    target="chart1",
                    mode="inline",
                    api="get: " + self.prefix + "/extra/list?starttime=${starttime}&endtime=${endtime}",
                    body=[
                        DateItem(
                            label="开始日期", name="starttime", value="-8days", maxDate="${endtime}",
                            format="YYYY-MM-DD", inputFormat="YYYY-MM-DD"
                        ), DateItem(
                            label="结束日期", name="endtime", value="-1days", minDate="${starttime}",
                            format="YYYY-MM-DD", inputFormat="YYYY-MM-DD"
                        )
                    ]
                ),
                Divider(),
                Chart(
                    name="chart1",
                    api="get: " + self.prefix + "/extra/list?starttime=${starttime}&endtime=${endtime}",
                )
            ]
        )
