from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import LongToShort

#from django.contrib.gis.geoip2 import GeoIP2
from django_user_agents.utils import get_user_agent


# Create your views here.
def hello_world(request):
    return HttpResponse("Hello World!")

def home_page(request):

    context = {"submitted": False, "error": False} 

    if request.method == 'POST':
        
        data = request.POST
        long_url = data["longurl"]
        custom_name = data["custom_name"]
       
        try:
            #CREATE
            obj = LongToShort(long_url = long_url, short_url = custom_name)
            obj.save()

            #READ
            date = obj.date
            clicks = obj.clicks

            context["long_url"] = long_url
            context["short_url"] = request.build_absolute_uri() + custom_name
            context["date"] = date
            context["clicks"] = clicks
            context["submitted"] = True

        except:
            context["error"] = True

    return render(request, 'index.html', context)


def redirect_url(request, shorturl):
    row = LongToShort.objects.filter(short_url = shorturl)
    
    
    if len(row) == 0:
        return HttpResponse("No such short url exists!!")
    
    print("row = ",row[0])
    
    obj = row[0]
    long_url = obj.long_url
    obj.clicks = obj.clicks + 1
   
    obj.save()

    return redirect(long_url)

def all_analytics(request):
    rows = LongToShort.objects.all()

    context = {"rows": rows}
    return render(request, 'all-analytics.html', context)

def single_analytics(request,shorturl):
    rows = LongToShort.objects.filter(short_url=shorturl)
    obj=rows[0]
    long_url = obj.long_url
    short_url = obj.short_url
    date=obj.date
    clicks=obj.clicks
    
    

    # user_agent = request.META['HTTP_USER_AGENT']
    # print("user_agent: ",user_agent)

    # if 'Mobile' in user_agent:
    #     print("Mobile")
    #     obj.mobile = obj.mobile + 1
    # else:
    #     obj.desktop = obj.desktop + 1

    user_agent = get_user_agent(request)
    print("User Agent: " , user_agent)
    if user_agent.is_mobile or 'Mobile' in str(user_agent):
        obj.mobile = obj.mobile + 1
    elif user_agent.is_tablet or user_agent.is_pc:
        obj.desktop = obj.desktop + 1

    obj.clicks =  obj.mobile + obj.desktop

    print("mobile = ",obj.mobile," and desktop = ", obj.desktop)
    context = {"short_url": short_url, "long_url": long_url, "date": date, "clicks": clicks, "mobile": obj.mobile, "desktop": obj.desktop}
    obj.save()


    # g = GeoIP2()
    # remote_addr = request.META.get('HTTP_X_FORWARDED_FOR')
    # if remote_addr:
    #     address = remote_addr.split(',')[-1].strip()
    # else:
    #     address = request.META.get('REMOTE_ADDR')
    # country = g.country_code(address)
    # print("c = " , country)
    

    return render(request,"analytics.html", context)