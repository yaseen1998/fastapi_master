import time
from newmain import redis,Product

key ='order-completed'
group = 'warehose-group'

try:
    redis.xgroup_create(name=key,groupname=group,mkstream=True)
    print('group created')
except Exception as e:
    print(str(e))
    
    
while True:
    try:
        results = redis.xreadgroup(groupname=group,consumername=key,streams={key:'>'})
        print(results)
        if len(results) > 0:
            for result in results:
                obj = result[1][0][1]
                try :
                    product = Product.get(pk=obj['product_id'])
                    product.quqntity -= int(obj['quantity'])
                    product.save()
                    print(product)
                except Exception as e:
                    redis.xadd(name='refund-order', fields=obj)
    except Exception as e:
        print(str(e))
    time.sleep(3)