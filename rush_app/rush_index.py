# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Members
from models import Rushset
from django.utils import timezone
from datetime import datetime, timedelta
import time
import json
#from rushset import 

def rush_index(request):
    err = ""
    if request.method == "POST":
        rush_id = 0
        #for i in request.POST.items():
            #if i[0].startswith("rushid"):
                #rush_id = int(i[0].split("_")[1])
                #break
        #rush_id = 2
        rush_id = int(request.POST.get("rushid"))
        #rush = Rushset.objects.filter(id=rush_id)[0]
        #if rush.is_finish:
            #request.session["err"] = "%s秒杀已经结束，请期待下一轮秒杀" % rush.rush_name.encode("utf8")
            #return HttpResponseRedirect("./")
        #else:
            #request.session["rush_id"] = rush_id
            #return HttpResponseRedirect("/rush")
        
        request.session["rush_id"] = rush_id
        return HttpResponseRedirect("/rush")        
            
    else:
        err = request.session.get("err", "")
        if err:
            request.session.pop("err")
        rush_number = 0
        rush_button = "hidden"
        dis_day = "00"
        dis_hour = "00"
        dis_min = "00"
        dis_sec = "00"
        total_sec = 0
        result = Rushset.objects.order_by("started_at").filter(is_finish=0, started_at__gte = datetime.now() - timedelta(seconds = 300))
        if len(result) != 0:
            rush_number = 1
            rush = result[0]
            now_time = datetime.now()
            if rush.started_at > now_time:
                total_sec = int((rush.started_at - now_time).total_seconds())
                #print total_sec
                dis_day = total_sec / 86400
                dis_day = dis_day if dis_day >= 10 else "0%s" % str(dis_day)
                dis_hour = total_sec / 3600 % 24
                dis_hour = dis_hour if dis_hour >= 10 else "0%s" % str(dis_hour)
                dis_min = total_sec / 60 % 60
                dis_min = dis_min if dis_min >= 10 else "0%s" % str(dis_min)
                dis_sec = total_sec % 60
                dis_sec = dis_sec if dis_sec >= 10 else "0%s" % str(dis_sec)
                rush_button = "hidden"
            else:
                rush_button = "visible"
    
            start_at = "%s/%s/%s %s:%s:%s" % (rush.started_at.year, rush.started_at.month, rush.started_at.day, rush.started_at.hour, rush.started_at.minute, rush.started_at.second)      
            now = now_time.strftime('%Y/%m/%d %H:%M:%S');
        return render_to_response("index.html", locals(), context_instance = RequestContext(request))        
        


