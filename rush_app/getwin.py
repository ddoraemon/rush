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
def getwin(request):
    err = ""
    if request.method == "POST":
        member_id = request.POST.get("member_id")
        do = request.POST.get("sub")
        if do == "确认中奖".decode("utf8"):
            is_win = 1
            fun = "save"
        elif do == "取消中奖".decode("utf8"):
            is_win = 0
            fun = "save"
        elif do == "删除该号".decode("utf8"):
            is_win = 0
            fun = "delete"
        
        member = Members.objects.filter(id = int(member_id))[0]
        member.is_rush_secceed = is_win
        process = getattr(member, fun)
        process()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/login'))
    elif request.method == "GET":
        if request.session.get("admin", None):
            rush_id = request.GET.get("id", None)
            return get_win_table(request, rush_id)
        else:
            request.session["current_page"] = request.META.get('HTTP_REFERER', '/getwin')
            return HttpResponseRedirect("/login")
        
        
        
def get_win_table(request, rush_id):
    show_list = []
    rushset = Rushset.objects.all()
    if rush_id != None:
        rushset_list = rushset.filter(id = int(rush_id))
    else:
        rushset_list = rushset
        
    for rush in rushset_list:
        win_list = []
        win_list.append(rush.rush_name)
        members = Members.objects.order_by("created_at").filter(rushset_id = rush.id)[:rush.rush_count]
        win_list.append(members)
        show_list.append(win_list)
    return render_to_response("getwin.html", locals(), context_instance = RequestContext(request))
    