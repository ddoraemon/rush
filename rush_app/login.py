# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Members
from models import Rushset
from django.utils import timezone
from datetime import datetime
import time
import json
import copy
from django.db.utils import IntegrityError
from random import *
def login(request):
    err = ""
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        if username == "admin" and password == "19283746":
            page = request.session.get("current_page", "/getwin")
            request.session["admin"] = True
            request.session.set_expiry(18000)
            return HttpResponseRedirect(page)
        else:
            request.session["login_err"] = "请输入正确的用户名和密码"
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    elif request.method == "GET":
        err = request.session.get("login_err", "")
        if err:
            request.session.pop("login_err")
        return render_to_response("login.html", locals(), context_instance = RequestContext(request))
        
        
        
def rush_register(phone, rush_id):
    msg = ""
    member_insert = Members(phone = phone, rushset_id = rush_id, is_rush_secceed = 0, created_at = datetime.now())
    rushset_obj = Rushset.objects.filter(id = rush_id)[0]
    if rushset_obj.is_finish:
        return False, "抱歉亲，您手慢了，本轮秒杀已经结束..."
    else:
        member_list = Members.objects.filter(rushset_id = rush_id)
        if len(member_list) < rushset_obj.rush_count + 3:
            member_insert.save()
            if len(member_list) == rushset_obj.rush_count + 2:
                rushset_obj.is_finish = 1
                rushset_obj.save()
            return True, "恭喜您进入中奖名单，不过还得看排名哦"
        else:
            rushset_obj.is_finish = 1
            rushset_obj.save()            
            return False, "抱歉亲，您手慢了，本轮秒杀已经结束..."