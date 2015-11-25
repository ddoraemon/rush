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
def rushgo(request):
    if request.method == "POST":
        result = False
        msg = ""
        rush_id = request.session.get("rush_id", None)
        if rush_id == None:
            request.session["err"] = "秒杀超时"
            return HttpResponseRedirect("/index")        
        phone = request.POST.get("phone")
        member = Members.objects.filter(phone=phone)
        if len(member) == 0:
            result, msg = rush_register(phone, rush_id)
        else:
            if len(member.filter(is_rush_secceed = 1)) == 0:
                if len(member.filter(rushset_id = rush_id)) == 0:
                    result, msg = rush_register(phone, rush_id)
                else:
                    result = False
                    msg = "您已经参与过本轮秒杀，谢谢参与 ^_^"
            else:
                result = False
                msg = "亲您已经中奖过了，谢谢参与 ^_^"
        request.session["err"] = msg
        return HttpResponseRedirect("/index")
    elif request.method == "GET":
        rush_id = request.session.get("rush_id", None)
        if rush_id == None:
            request.session["err"] = "秒杀超时"
            return HttpResponseRedirect("/index")
        else:
            number_list = [randint(1, 3) for i in range(3)]
            puzzle = "%s + %s x %s" % tuple(number_list)
            reuslt = number_list[0] + number_list[1] * number_list[2]
            return render_to_response("rushgo.html", locals(), context_instance = RequestContext(request))
        
        
def rush_register(phone, rush_id):
    msg = ""
    member_insert = Members(phone = phone, rushset_id = rush_id, is_rush_secceed = 0, created_at = datetime.now())
    rushset_obj = Rushset.objects.filter(id = rush_id)
    
    if len(rushset_obj) == 0 or rushset_obj[0].is_finish:
        return False, "抱歉亲，您手慢了，本轮秒杀已经结束..."
    else:
        rushset_obj = rushset_obj[0]
        member_list = Members.objects.filter(rushset_id = rush_id)
        if len(member_list) < rushset_obj.rush_count:
            member_insert.save()
            if len(member_list) == rushset_obj.rush_count - 1:
                rushset_obj.is_finish = 1
                rushset_obj.save()
            return True, "恭喜您进入中奖名单，不过还得看排名哦"
        else:
            rushset_obj.is_finish = 1
            rushset_obj.save()
            return False, "抱歉亲，您手慢了，本轮秒杀已经结束..."