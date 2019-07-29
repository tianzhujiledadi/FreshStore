import time
#装饰器
def tb(f):#装饰器的函数，f接受被装饰的函数名
    print('装饰器头部')
    def nb():#装饰内部函数
        start=time.time()
        f()#调用被装饰的函数
        end=time.time()
        print(end-start)
        #print('装饰器')
    return nb#装饰器返回内部函数(内部代表的是包装盒)
#return返回什么这个函数就等于什么
@tb#@加函数名,代表下面的函数被该函数装饰即f=zs,也就是该函数的形参是是下面个函数的函数名，然后在调用该函数
def zs():
    print('被装饰的内容')
zs()