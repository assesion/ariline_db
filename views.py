from django.shortcuts import render
from app01 import models
from django.shortcuts import redirect
from app01 import forms
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.


def index(request):
    pass
    return render(request, 'app01/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        message = '请检查填写的内容！'
        if username.strip() and password:
            try:
                user = models.User.objects.get(user=username)
            except :
                message = '用户不存在！'
                return render(request, 'app01/login.html', {'message': message})
            if user.passwd == password:
                print(username, password)
                request.session['is_login'] = True
                request.session['username'] = username
                request.session.set_expiry(600)   #保持600s
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'app01/login.html', {'message': message})
        else:
            return render(request, 'app01/login.html', {'message': message})
    return render(request, 'app01/login.html')


def register(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == 'POST':
        username = request.POST.get('Name')
        email = request.POST.get('Email')
        tel = request.POST.get('Tel')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        message = '请检查填写的内容！'
        if password != confirm_password:
            message = '两次输入密码不一致！'
            return render(request,'app01/register.html',{'message': message})
        else:
            same_name_user = models.User.objects.filter(user=username)
            if same_name_user:
                message = '用户名已经存在'
                return render(request, 'app01/register.html', {'message':message})
            same_email_user = models.User.objects.filter(mail=email)
            if same_email_user:
                message = '该邮箱已经被注册了！'
                return render(request, 'app01/register.html', {'message':message})
            new_user = models.User()
            new_user.user = username
            new_user.passwd = password
            new_user.mail = email
            new_user.tel = tel
            new_user.lx = "1"
            new_user.save()
            message = "注册成功！"
        return render(request, 'app01/register.html',{'message':message})
    return  render(request,'app01/register.html')


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.clear()
    return redirect('/index/')


def search(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    tickets = models.Hb.objects.all().values()
    if request.method == 'POST':
        qds = request.POST.get('qd')
        zds = request.POST.get('zd')
        print(zds)
        tickets_ = models.Hb.objects.filter(qd=qds,zd=zds)
        print (tickets_)
        return  render(request,'app01/search.html',{'hb':tickets_})
    return  render(request,'app01/search.html',{'hb':tickets})


def gp(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    if request.method == 'POST':
        hb = request.POST.get('bh')
        name = request.POST.get('name')
        tel_ = request.POST.get('tel')
        sfzh_ = request.POST.get('sfzh')
        hb_yp = models.Hb.objects.filter(bh=hb).values('yp')[0]['yp']
        hb_time = models.Hb.objects.filter(bh=hb).values('qfsj')[0]['qfsj']
        usr = request.session.get('username')
        print("ok")
        print(usr)
        print("ok")
        hb_time = hb_time.replace(tzinfo=None)
        print(usr)
        print(hb_time)
        time = datetime.now()
        print(type(time))
        print(time)
        print(hb_time-time)
        if hb_time-time < timedelta(hours=1):
            message="距离航班起飞时间在一小时之内，无法购买本次航班坐席！"
            return render(request, 'app01/search.html', {'message': message})
        if hb_yp > 0:
            models.Ydjl.objects.create(xm=name,user=usr,hbbh=hb,tel=tel_,sfzh=sfzh_,dpsj=time)
            models.Hb.objects.filter(bh=hb).update(yp=hb_yp - 1)
            message = "恭喜您购票成功，祝您旅途愉快！"
            return render(request,'app01/search.html',{'message':message})
    return render(request,'app01/search.html')



def jc_admin_add(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    usr = request.session.get('username')
    print(usr)
    lx = models.User.objects.filter(user=usr).values('lx')[0]['lx']
    print (lx)
    if not lx == "2":
        message = "无权限！"
        print(message)
        return redirect('/index/', {'message': message})
    tickets = models.Hb.objects.all().values()
    if request.method == 'POST':
        hb_ = request.POST.get('bh')
        qd_ = request.POST.get('qd')
        zd_ = request.POST.get('zd')
        qfsj_ = request.POST.get('qfsj')
        ddsj_ = request.POST.get('ddsj')
        hxbh_ = request.POST.get('hxbh')
        yp_  =  request.POST.get('yp')
        zp_ = request.POST.get('zp')
        pj_ = request.POST.get('pj')
        hb_find = models.Hb.objects.filter(bh=hb_)
        hx_find = models.Hx.objects.filter(hxbh=hxbh_)
        if hb_find:
            message = "航班已存在！请重新填写！"
            return  render(request,'app01/jc_admin_add.html',{"message":message})
        if not hx_find:
            message = "航线不存在！请重新填写！"
            return render(request, 'app01/jc_admin_add.html', {"message": message})
        if yp_>zp_:
            message = "余票不能大于总票数！请重新填写！"
            return render(request, 'app01/jc_admin_add.html', {"message": message})
        models.Hb.objects.create(bh=hb_,qd=qd_,zd=zd_,qfsj=qfsj_,ddsj=ddsj_,hxbh=hxbh_,yp=yp_,zp=zp_,pj=pj_)
        message = "添加成功！"
        return render(request, 'app01/jc_admin_add.html', {"message": message})
    return render(request,'app01/jc_admin_add.html',{'hb':tickets})


def  jc_admin_update(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    usr = request.session.get('username')
    print(usr)
    lx = models.User.objects.filter(user=usr).values('lx')[0]['lx']
    if not lx == "2":
        message = "无权限！"
        return redirect('/index/',{'message':message})
    tickets = models.Hb.objects.all().values()
    if request.method == 'POST':
        hb_ = request.POST.get('bh')
        qd_ = request.POST.get('qd')
        zd_ = request.POST.get('zd')
        qfsj_ = request.POST.get('qfsj')
        ddsj_ = request.POST.get('ddsj')
        hxbh_ = request.POST.get('hxbh')
        yp_ = request.POST.get('yp')
        zp_ = request.POST.get('zp')
        pj_ = request.POST.get('pj')
        hb_find = models.Hb.objects.filter(bh=hb_)
        hx_find = models.Hx.objects.filter(hxbh=hxbh_)
        if not hb_find:
            message = "航班不存在！请重新填写！"
            return  render(request,'app01/jc_admin_update.html',{"message":message})
        if not hx_find:
            message = "航线不存在！请重新填写！"
            return render(request, 'app01/jc_admin_update.html', {"message": message})
        models.Hb.objects.filter(bh=hb_).update(qd=qd_,zd=zd_,qfsj=qfsj_,ddsj=ddsj_,hxbh=hxbh_,yp=yp_,zp=zp_,pj=pj_)
        message = "修改成功！"
        return render(request, 'app01/jc_admin_update.html', {"message": message})
    return render(request, 'app01/jc_admin_update.html', {'hb': tickets})


def jc_admin_delete(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    usr = request.session.get('username')
    print(usr)
    lx = models.User.objects.filter(user=usr).values('lx')[0]['lx']
    if not lx == "2":
        message = "无权限！"
        return redirect('/index/', {'message': message})
    tickets = models.Hb.objects.all().values()
    if request.method == 'POST':
        hb_ = request.POST.get('bh')
        hb_find = models.Hb.objects.filter(bh=hb_)
        if not hb_find:
            message = "航班不存在！请重新填写！"
            return  render(request,'app01/jc_admin_delete.html',{"message":message})
        models.Hb.objects.filter(bh=hb_).delete()
        message = "删除成功！"
        return render(request, 'app01/jc_admin_delete.html', {"message": message})
    return render(request, 'app01/jc_admin_delete.html', {'hb': tickets})



def grzx(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    usr = request.session.get('username')
    print (usr)
    tickets = models.Ydjl.objects.filter(user=usr)
    print(type(tickets))
    print(tickets)
    if tickets:
        print(usr)
        if request.method == 'POST':
            td = request.POST.get('bh')
            sfzh_ = request.POST.get('sfzh')
            time = models.Hb.objects.filter(bh=td).values('qfsj')[0]['qfsj']
            print (time)
            sfzh = models.Ydjl.objects.filter(sfzh=sfzh_)
            time = time.replace(tzinfo=None)
            local_time = datetime.now()
            if time - local_time < timedelta(hours=2):
                message = "航班在两小时内起飞，无法办理退票业务！"
                return render(request,'app01/grzx.html',{'message':message})
            if not  sfzh:
                message = "没有找到身份证号%s的订票记录！"(sfzh_)
                return render(request,'app01/grzx.html',{'message':message})
            models.Ydjl.objects.filter(sfzh=sfzh_,hbbh=td).delete()
            hb_yp = models.Hb.objects.filter(bh=td).values('yp')[0]['yp']
            models.Hb.objects.filter(bh=td).update(yp=hb_yp + 1)
            message = "退票成功！"
            return  render(request,'app01/grzx.html',{'message':message})
        return  render(request,'app01/grzx.html',{'hb':tickets})
    else:
        message = "没有购票记录！"
        return  redirect('/search/',{'message':message})





