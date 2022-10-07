from email.headerregistry import Address
from turtle import update
from django.shortcuts import render


from .models import OrderUpdate, Product,Contact,Order,OrderUpdate
from math import ceil
import json
from PayTm import Checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';


def index(request):
    products = Product.objects.all()
    
    catprods = Product.objects.values()
    allProds=[]
    cats={item['category'] for item in catprods}
    for cat in cats:
        prods=Product.objects.filter(category=cat)
        n= len(prods)
        nSlides=n//4 + ceil((n/4)-(n//4))
        allProds.append([prods,range(1,nSlides),nSlides])
        params = {'allProds':allProds}

    
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))
    # allProds = [[products,range(1,nSlides),nSlides],[products,range(1,nSlides),nSlides]]
    # params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)




def contact(request):
    thank = False
    if request.method=='POST':
        
        name=request.POST.get('name','')
        phone=request.POST.get('phone','')
        email=request.POST.get('email','')
        desc=request.POST.get('desc','')
        contact=Contact(name=name,phone=phone,email=email,desc=desc)
        contact.save()
        thank=True
    return render(request, 'shop/contact.html',{'thank':thank})

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates,order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def search(request):
    return render(request, 'shop/search.html')

def productView(request,myid):
    product = Product.objects.filter(id=myid)
    
    return render(request, "shop/productView.html",{'product':product[0]})

def checkout(request):
    if request.method == 'POST':
        items_json= request.POST.get('itemsJson', '')
        name=request.POST.get('name','')
        email = request.POST.get('email','')
        amount = request.POST.get('amount', '')
        address= request.POST.get('address1','')+""+request.POST.get('address2','')
        city = request.POST.get('city','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        order=Order(items_json=items_json,name=name,email=email,address=address,city=city,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        #return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        param_dict = {

                'MID': 'WorldP64425807474247',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request,'shop/paytm.html',{'param_dict':param_dict})

    return render(request, 'shop/checkout.html')

@csrf_exempt
def handlerequest(request):
    return HttpResponse('done')
    pass
def about(request):
    return render(request, 'shop/about.html')