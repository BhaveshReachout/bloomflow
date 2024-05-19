from django.shortcuts import render
from .render import Render
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from .utils import render_to_pdf
from .models import Profile, Product, Category, Contact, CartAdd, CartManager, Subcategory, Product_Gallary, Order, OrderDetails
from .forms import ProfileForm, SubcategoryForm, ProductForm, CartAddForm
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views.generic.edit import DeleteView
from django.views.generic import View
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login as login_process, logout, authenticate
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template
from django.contrib import messages
from .paytm import generate_checksum, verify_checksum
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def product_page(request, id):
    sc_list = Subcategory.objects.filter(category=1)
    sc1 = Subcategory.objects.filter(id=id)
    s = str(sc1)
    s1 = s[25:-3]
    s2 = s1 + '.html'
    return render(request, 'app1/'+s2, {"sc_list": sc_list})


def home(request):
    sc = Subcategory.objects.all()
    return render(request, 'app1/index.html', {'sc': sc})


def about_us_view(request):
    return render(request, 'app1/about_us.html')


def contact_us_view(request):
    return render(request, 'app1/contact_us.html')


def caretools_product_view(request):
    sc = Subcategory.objects.all()
    return render(request, 'app1/caretools_product.html', {'sc': sc})


def plants_detail_view(request, id=None):
    sc = Subcategory.objects.all()
    uid = request.user.id
    co = None
    if uid != None:
        user = User.objects.get(id=uid)
        co = CartAdd.objects.get(user=user)
    prod_d = Product.objects.get(id=id)
    prod_g = Product_Gallary.objects.get(Productid=prod_d)
    return render(request, 'app1/plants_detail.html', {'sc': sc, 'co': co, 'prod_d': prod_d, 'prod_g': prod_g})


def cart_view(request):
    cat_list = Category.objects.all()
    form = CartAddForm()
    cart_id = request.session.get('cart_id', None)
    uid = request.user.id
    if (uid is None):
        return signup_view(request)
    else:
        user = User.objects.get(id=uid)
        ca = CartAdd.objects.filter(user=user)
        if (ca.count() == 1):
            co = CartAdd.objects.get(user=user)
            ca1 = co.is_order
            cop = co.get_product()
            temp = 0
            if request.method == 'POST':
                form = CartAddForm(request.POST, request.FILES)
                if form.is_valid():
                    pass
                qty = request.POST.get('quantity')
                pid = request.POST.get('product_id')
                for i in cop:
                    if int(i.id) == int(pid):
                        temp_price = i.Pprice * int(qty)
                        temp = temp_price
                        co.set_total(temp)
                co.set_qty(int(qty))
            if (ca1):
                cid = CartAdd.objects.get(user=user)
        else:
            cart_obj = CartAdd.objects.new(user=request.user)
            cart_obj.is_order = True
            cop = None
            co = None

    cat_list = Category.objects.all()
    return render(request, 'app1/cart.html', {'cop': cop, 'co': co, 'cat_list': cat_list, 'form': form})


def order_view(request):
    uid = request.user.id
    user = User.objects.get(id=uid)
    o_list = Order.objects.all()
    od_list = OrderDetails.objects.get(order=19)
    o_prod = od_list.get_product()
    return render(request, 'app1/order.html', {'o_prod': o_prod})


def tempo_view(request, id=None):
    cat_list = Category.objects.all()
    cart_id = request.session.get('cart_id', None)
    uid = request.user.id
    if (uid is None):
        return signup_view(request)
    else:
        user = User.objects.get(id=uid)
        ca = CartAdd.objects.filter(user=user)
        if (ca.count() == 1):
            co = CartAdd.objects.get(user=user)
            ca1 = co.is_order
            cop = co.get_product()
            temp = 0
            t = 0
            if request.method == 'POST':
                form = CartAddForm(request.POST, request.FILES)
                if form.is_valid():
                    pass
                qty = request.POST.get('quantity')
                pid = request.POST.get('product_id')
                for i in cop:
                    if int(i.id) == int(pid):
                        temp_price = i.Pprice * int(qty)
                        temp = temp_price
                        i.set_prod_total(temp)
                        i.set_prod_qty(int(qty))

            for i in cop:
                t += i.Ptotal
            co.set_total(t)
            prod = Product.objects.get(id=id)
            co.product.add(prod)
            if (ca1):
                cid = CartAdd.objects.get(user=user)
        else:
            cart_obj = CartAdd.objects.new(user=request.user)
            cart_obj.is_order = True
            cop = None
            co = None
    return render(request, 'app1/cart.html', {'cop': cop, 'co': co, 'cat_list': cat_list})


def cart_remove_view(request, id=None):
    uid = request.user.id
    user = User.objects.get(id=uid)
    cart = CartAdd.objects.get(user=user)
    pod = Product.objects.get(id=id)
    cart.product.remove(pod)
    return cart_view(request)


@login_required
def checkout_view(request):
    pro1 = None
    user = request.user
    cart_obj = CartAdd.objects.get(user=user)
    amount = cart_obj.get_total()
    cop = cart_obj.get_product()
    if Profile.objects.filter(user=user).count() == 1:
        pro1 = Profile.objects.get(user=user)
    if (request.method == 'POST'):
        user = request.user
        p_mode = request.POST.get('p_mode')
        ocontactno = request.POST.get('Pnumber')
        address = request.POST.get('Address')
        pro1.set_order_data(a=address)
        cart_obj = CartAdd.objects.get(user=user)
        cart = cart_obj
        cop = cart_obj.get_product()
        o1 = Order.objects.create(made_by=user, cart=cart_obj, amount=amount,
                                  p_mode=p_mode, ocontactno=ocontactno, oaddress=address)
        o1.save()
        merchant_key = settings.PAYTM_SECRET_KEY
        params = (
            ('MID', settings.PAYTM_MERCHANT_ID),
            ('ORDER_ID', str(o1.order_id)),
            ('CUST_ID', str(o1.made_by.email)),
            ('TXN_AMOUNT', str(o1.amount)),
            ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
            ('WEBSITE', settings.PAYTM_WEBSITE),
            ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
            ('CALLBACK_URL', 'http://127.0.0.1:8000/app1/callback/'),
        )
        paytm_params = dict(params)
        checksum = generate_checksum(paytm_params, merchant_key)
        o1.checksum = checksum
        o1.save()

        paytm_params['CHECKSUMHASH'] = checksum
        return render(request, 'app1/redirect.html', context=paytm_params)
    return render(request, 'app1/checkout.html', {'pro1': pro1, 'cop': cop, 'cart_obj': cart_obj})


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(
            paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'app1/callback.html', context=received_data)
        return render(request, 'app1/callback.html', context=received_data)


def caretools_view(request):
    sc = Subcategory.objects.all()
    return render(request, 'app1/caretools.html', {'sc': sc})


def gifts_view(request):
    sc = Subcategory.objects.all()
    return render(request, 'app1/gifts.html', {'sc': sc})


def gifts_product_view(request):
    sc = Subcategory.objects.all()
    return render(request, 'app1/gifts_product.html', {'sc': sc})


def learn_view(request):
    return render(request, 'app1/learn.html')


def signup_view(request):
    if (request.method == 'POST'):
        RF = RegistrationForm(request.POST)
        if (RF.is_valid()):
            RF.save(request)
            return HttpResponseRedirect(reverse('login'))
        else:
            HttpResponse("invalid Data")
            HttpResponse(RF.errors)
    else:
        RF = RegistrationForm()
    return render(request, 'signup.html', {'RF': RF})


class EmailAuthBackend:
    def authenticate(username, password, backend):
        try:
            user = User.objects.get(email=username)
            success = user.check_password(password)
            if success:
                return user
        except User.DoesNotExist:
            pass
        return None


def user_login(request):
    session_var = request.session.items()
    if request.session.has_key('uname') and request.session.has_key('password'):
        uname = request.session['uname']
        pwd = request.session['password']
        a1 = EmailAuthBackend
        user = a1.authenticate(username=uname, password=pwd,
                               backend='django.contrib.auth.backends.ModelBackend')
        login_process(
            request, user, 'django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(reverse_lazy('index'))
    else:
        return user_login1(request)


def user_login1(request):
    uname = ''
    pwd = ''
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remind = request.POST.get('remember_me')
        a1 = EmailAuthBackend
        user = a1.authenticate(username=username, password=password,
                               backend='django.contrib.auth.backends.ModelBackend')
        if user:
            if (user.is_active):
                login_process(
                    request, user, 'django.contrib.auth.backends.ModelBackend')
                if remind:
                    request.session['uname'] = username
                    request.session['password'] = password
                return home(request)
            else:
                return HttpResponse('user is not active')
        else:
            return HttpResponse('invalid username and password')

    return render(request, 'login.html', {'uname': uname, 'pwd': pwd})


@login_required
def user_logout(request):
    data_key = request.session.items()
    uname = request.session.get('uname')
    pwd = request.session.get('password')
    logout(request)
    if uname and pwd:
        request.session['uname'] = uname
        request.session['password'] = pwd
    return render(request, 'app1/index.html')


@login_required
def profile_final_view(request):
    p2 = None
    global form_pic
    form_pic = None
    user = request.user
    pr = Profile.objects.filter(user=user)
    if request.method == 'POST':
        if pr.count() is not 0:
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                form_pic = form.cleaned_data.get('picture')
            p1 = Profile.objects.get(user=user)
            n = request.POST.get('name')
            add = request.POST.get('address')
            p = request.POST.get('picture')
            if p1 is not None:
                p1.set_data(n, form_pic, add)
                messages.success(
                    request, 'profile update successfull', extra_tags='alert')
                return redirect('profile')
        else:
            p1 = Profile.objects.create(user=user)
            n = request.POST.get('name')
            add = request.POST.get('address')
            if p1 is not None:
                if p1.set_data(n, form_pic, add) == 'done':
                    pr = 1
                    return HttpResponse("profile update successfully")
                else:
                    return HttpResponse("profile is not updated")
    if Profile.objects.filter(user=user).count() is not 0:
        p2 = Profile.objects.get(user=user)
    form = ProfileForm()
    return render(request, 'app1/profile_final.html', {'p2': p2, 'form': form})


@login_required
def profile_final_edit_view(request):
    p2 = None
    global form_pic
    form_pic = None
    user = request.user
    pr = Profile.objects.filter(user=user)
    if request.method == 'POST':
        if pr.count() is not 0:
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                form_pic = form.cleaned_data.get('picture')
            p1 = Profile.objects.get(user=user)
            n = request.POST.get('name')
            add = request.POST.get('address')
            if p1 is not None:
                p1.set_data(n, form_pic, add)
                messages.success(
                    request, 'profile update successfull', extra_tags='alert')
                return redirect('profile_final')
        else:
            p1 = Profile.objects.create(user=user)
            n = request.POST.get('name')
            add = request.POST.get('address')
            if p1 is not None:
                if p1.set_data(n, form_pic, add) == 'done':
                    pr = 1
                    return HttpResponse("profile update successfully")
                else:
                    return HttpResponse("profile is not updated")
    if Profile.objects.filter(user=user).count() is not 0:
        p2 = Profile.objects.get(user=user)
    form = ProfileForm()
    return render(request, 'app1/profile_edit_final.html', {'p2': p2, 'form': form})


def master_view(request):
    pro = Product.objects.all()
    cat_list = Category.objects.all()
    return render(request, "app1/master.html", {'pro': pro, 'cat_list': cat_list})


def plants_view(request):
    prod = Product.objects.all()
    sc = Subcategory.objects.all()
    return render(request, 'app1/plants.html', {'prod': prod, 'sc': sc})


class GeneratePDF(View):
    template = get_template('app1/invoice.html')
    context_object_name = 'order'
    models = Order

    def get(self, request, *args, **kwargs):

        context = {
            "invoice_id": 123,
            "customer_name": "John",
            "amount": 125,
            "today": "today",
        }
        return Render.render('app1/invoice.html', {'context': context})


class SearchProductView(ListView):
    template_name = 'app1/product_search.html'
    context_object_name = 'prod'
    models = Product
    cat_list = Category.objects.all()
    prod = Product.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        si = self.request.GET.get('si')
        if si == None:
            si = ''

    def get_queryset(self, *args, **kwargs):
        request = self.request
        si = request.GET.get('si')
        if si == None:
            si = ''
        cat_list = Category.objects.all()
        return Product.objects.filter(Pname__icontains=si)

    def get_context_data(self, **kwargs):
        context = super(SearchProductView, self).get_context_data(**kwargs)
        context.update({
            'cat_list': Category.objects.all()
        })
        return context
