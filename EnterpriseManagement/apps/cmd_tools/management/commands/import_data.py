import os
import sys
import json

from django.core.management.base import BaseCommand


def set_env():
    pwd = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(pwd)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoShop.settings")

    import django
    django.setup()


def import_goods_data():
    from goods.models import Goods, GoodsCategory, GoodsImage

    with open('data/product_data.json', 'r', encoding='utf8') as f:
        row_data = json.loads(f.read())

    for goods_detail in row_data:
        goods = Goods()
        goods.name = goods_detail["name"]
        goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
        goods.shop_price = float(int(goods_detail["sale_price"].replace("￥", "").replace("元", "")))
        goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
        goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
        goods.goods_front_image = goods_detail["images"][0] if goods_detail["images"] else ""

        category_name = goods_detail["categorys"][-1]
        category = GoodsCategory.objects.filter(name=category_name)
        if category:
            goods.category = category[0]
        goods.save()

        for goods_image in goods_detail["images"]:
            goods_image_instance = GoodsImage()
            goods_image_instance.image = goods_image
            goods_image_instance.goods = goods
            goods_image_instance.save()


def import_category_data():
    from goods.models import GoodsCategory

    with open('data/category_data.json', 'r', encoding='utf8') as f:
        row_data = json.loads(f.read())

    for lev1_cat in row_data:
        lev1_intance = GoodsCategory()
        lev1_intance.code = lev1_cat["code"]
        lev1_intance.name = lev1_cat["name"]
        lev1_intance.category_type = 1
        lev1_intance.save()

        for lev2_cat in lev1_cat["sub_categorys"]:
            lev2_intance = GoodsCategory()
            lev2_intance.code = lev2_cat["code"]
            lev2_intance.name = lev2_cat["name"]
            lev2_intance.category_type = 2
            lev2_intance.parent_category = lev1_intance
            lev2_intance.save()

            for lev3_cat in lev2_cat["sub_categorys"]:
                lev3_intance = GoodsCategory()
                lev3_intance.code = lev3_cat["code"]
                lev3_intance.name = lev3_cat["name"]
                lev3_intance.category_type = 3
                lev3_intance.parent_category = lev2_intance
                lev3_intance.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        set_env()

        import_category_data()
        import_goods_data()
