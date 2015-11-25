# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Members
from models import Rushset
from django.utils import timezone
from datetime import datetime, timedelta
import time
import json
import copy
from django.db.utils import IntegrityError
def rushset(request, *test, **ttest):
    def get_html(request, add_err = False, err = ""):
        now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()).split("-")
        year_list = map(lambda x:str(x), range(int(now[0]), int(now[0]) + 3))
        rush_list = Rushset.objects.order_by("started_at")
        return render_to_response("rushset.html", locals(), context_instance = RequestContext(request))
    print request.POST.items()
    add_err = False
    err = ""
    
    if request.method == "POST":
        try:
            print request.POST
            if request.POST.get("sub") == "Add":
                add_err, err, arg_dict = add_arg_check(request.POST.items())
                
                rush_name, year, month, day, hour, minute, second, rush_count = (arg_dict["rush_name"], int(arg_dict["year"]), int(arg_dict["month"]), 
                                                                                 int(arg_dict["day"]), int(arg_dict["hour"]), int(arg_dict["min"]), 
                                                                                 int(arg_dict["sec"]), int(arg_dict["rush_count"]))
                if_finish = 1 if datetime.now() > datetime(year, month, day, hour, minute, second, 0) else 0
                
                new_rush = Rushset(rush_name = rush_name, is_finish = if_finish, rush_count = rush_count, 
                                   started_at = datetime(year, month, day, hour, minute, second, 0),
                                   updated_at = datetime.now(), created_at = datetime.now()) 
                try:
                    new_rush.save()
                except IntegrityError, ex:
                    if "Duplicate entry" in str(ex):
                        raise Exception("名为%s的秒杀已经存在，请重新设置秒杀名" % arg_dict["rush_name"].encode("utf8"))
                    else:
                        raise Exception(str(ex))
            elif request.POST.get("sub") == "QuickStart":
                rush_count = int(request.POST.get("rush_count"))
                rush_start_time = int(request.POST.get("rush_start_time"))
                rush_name = "第%s轮" % str(len(Rushset.objects.all()) + 1).encode("utf8")
                
                new_rush = Rushset(rush_name = rush_name, is_finish = 0, rush_count = rush_count, 
                                   started_at = datetime.now() + timedelta(seconds = rush_start_time),
                                   updated_at = datetime.now(), created_at = datetime.now()) 
                try:
                    new_rush.save()
                except IntegrityError, ex:
                    print str(ex)
                    if "Duplicate entry" in str(ex):
                        raise Exception("名为%s的秒杀已经存在，请重新设置秒杀名" % rush_name)
                    else:
                        raise Exception(str(ex))                
                
                
                    
            elif request.POST.get("sub") == "Finish":
                pj = Rushset.objects.filter(id = int(request.POST.get("rush_id")))
                if len(pj) != 0:
                    pj[0].is_finish = 1
                    pj[0].save()
            elif request.POST.get("sub") == "Delete":
                pj = Rushset.objects.filter(id = int(request.POST.get("rush_id")))
                if len(pj) != 0:
                    pj[0].delete()
                members_list = Members.objects.filter(rushset_id = int(request.POST.get("rush_id")))
                for member in members_list:
                    member.delete()
        except Exception, ex:
            request.session["rushset_err"] = str(ex)
            #return get_html(request, True, str(ex))
            return HttpResponseRedirect("/rushset")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    elif request.method == "GET":
        if request.session.get("admin", None) == None:
            request.session["current_page"] = request.META.get('HTTP_REFERER', '/rushset')
            return HttpResponseRedirect("/login")
        err = request.session.get("rushset_err", "")
        if err:
            request.session.pop("rushset_err")
        return get_html(request, False, err)

    

def add_arg_check(arg_list):
    err = False
    err_msg = ""
    arg_dict = {}
    for k,v in arg_list:
        try:
            if k == "rush_name":
                if v == "":
                    raise Exception("请输入秒杀名")
                else:
                    arg_dict[k] = v
            elif k in ["year", "month", "day", "hour", "min", "sec"]:
                if v == "":
                    raise Exception("请输入时间")
                else:
                    arg_dict[k] = v
            elif k == "rush_count":
                if v == "":
                    raise Exception("请输入中奖人数")
                else:
                    try:
                        int(v)
                        arg_dict[k] = v
                    except ValueError,ex:
                        raise Exception("中奖人数请输入数字")                    
            else:
                arg_dict[k] = v
        except Exception,ex:
            err = True
            err_msg = ex
            arg_dict = {}
            raise Exception(err_msg)
    return err, err_msg, arg_dict
    