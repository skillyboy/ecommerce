from .models import Shopcart, Category, Carousel


def cartread(request):
    cart=Shopcart.objects.filter(user__username=request.user.username, paid_order=False)


    cartreader=0
    for item in cart:
        cartreader += item.quantity

    context={
        'cartreader':cartreader
    }
    return context
    

def dropdown(request):
    categories = Category.objects.all()

    context = {
        'categories':categories
    }

    return context
    

def banner(request):
    slide= Carousel.objects.get(pk=1)
    slide2=Carousel.objects.get(pk=2)
    slide3=Carousel.objects.get(pk=3)


    context={
        'slide':slide,
        'slid2':slide2,
        'slide3':slide3,
    }

    return context