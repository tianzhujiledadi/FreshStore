from  Store.models import Goods
from  django.db.models import Sum,Avg,F,Q
print(Goods.objects.filter(goods_price__gt=100).values("goods_name"))