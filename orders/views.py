from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView, View, CreateView, DetailView
from decimal import Decimal

from .models import Customer, Category, Item, Order, ShoppingCart, ItemExtra, ItemOption, OrderItem
from .models import Contact, IndexShelf
# Create your views here.
class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "orders/index.html", context={"object_list": IndexShelf.objects.all()})

class ContactView(View):

    def get(self, request, *args, **kwargs):
        contacts = Contact.objects.all()
        return render(request, "orders/contact.html", context={"object": contacts[0]})

class MenuView(ListView):
    model = Category
    template_name = "orders/menu.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'customer_id' in self.request.session:
            context["order_count"] = Order.objects.filter(created_by=self.request.session['customer_id'], status__in=["new", "pending"]).count()
            context["shopping_count"] = ShoppingCart.objects.filter(user=self.request.session['customer_id']).count()
        context["item_list"] = Item.objects.all()
        return context 

class ItemView(DetailView):
    model = Item
    template_name = "orders/item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_option_query_set = ItemOption.objects.filter(item=self.object.id)
        item_option_ids = [ option['id'] for option in item_option_query_set.values("id")]
        context["item_option_list"] = item_option_query_set
        context["item_extra_list"] = ItemExtra.objects.filter(item_option__in=item_option_ids)
        return context 

class SignInView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "orders/sign_in.html")
    
    def post(self, request, *args, **kwargs):
        form = request.POST
        try:    
            c = Customer.objects.get(username=form['username'])
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, "Username does not exist.")
            return redirect("/login")
        if c.password == form['password']:
            request.session['customer_id'] = c.id
            request.session['customer_name'] = c.username
            messages.add_message(request, messages.SUCCESS, "Login success.")
            return redirect("/")
        else:
            messages.add_message(request, messages.ERROR, "Password does not match.")
            return redirect("/login")

class SignUpView(CreateView):
    model = Customer
    fields = ['username', 'first_name', 'last_name', 'email', 'password']
    success_url = "/login"

    def get(self, request, *args, **kwargs):
        return render(request, "orders/sign_up.html")

class ShoppingCartView(CreateView):
    model = ShoppingCart
    fields = ['item_option', 'item_extra', 'user', 'item_num']
    success_url = "/shoppingcart"
    template_name = "orders/shopping_cart.html"

    def get(self, request, *args, **kwargs):
        context = {}
        if 'customer_id' not in request.session:
            messages.add_message(request, messages.ERROR, "You should login to web firstly.")
            return redirect("/login")
        if 'cart_id' in request.GET:
            ShoppingCart.objects.get(pk=request.GET["cart_id"]).delete()
        object_list = ShoppingCart.objects.filter(user=request.session['customer_id'])
        for obj in object_list:
            amount = obj.item_option.price
            for extra in obj.item_extra.all():
                amount = amount + extra.cost
            obj.amount = amount * obj.item_num
        context["object_list"] = object_list
        return render(request, "orders/shopping_cart.html", context=context)

    def post(self, request, *args, **kwargs):
        if 'customer_id' not in request.session:
            messages.add_message(request, messages.ERROR, "You should login to web firstly.")
            return redirect("/login")
        return super().post(request, *args, **kwargs)

class OrderView(ListView):
    model = Order
    template_name = "orders/order.html"

    def get(self, request, *args, **kwargs):
        if 'customer_id' not in request.session:
            messages.add_message(request, messages.ERROR, "You should login to web firstly.")
            return redirect("/login")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order_query_set = Order.objects.filter(created_by=self.request.session['customer_id'])
        context["order_list"] = order_query_set
        order_details = []
        for order in order_query_set:
            order_details.append({"order_id":order.id, "detail":order.get_item_detail()})
        context["order_details"] = order_details
        return context

    def post(self, request, *args, **kwargs):
        if 'customer_id' not in request.session:
            messages.add_message(request, messages.ERROR, "You should login to web firstly.")
            return redirect("/login")
        carts = ShoppingCart.objects.filter(user=request.session['customer_id'])
        if not carts:
            messages.add_message(request, messages.ERROR, "Your shopping cart is empty.")
            return redirect("/menu")
        amount = Decimal()
        order_obj = Order(created_by=Customer.objects.get(pk=request.session['customer_id']), amount=amount)
        order_obj.save()
        for cart in carts:
            OrderItem(order=order_obj, item_type="option",
            item_id=cart.item_option.id, item_cost=cart.item_option.price,
            item_num=cart.item_num).save()
            amount = amount + cart.item_option.price * cart.item_num
            for extra in cart.item_extra.all():
                OrderItem(order=order_obj, item_type="extra",
                item_id=extra.id, item_cost=extra.cost).save()
                amount = amount + extra.cost
        order_obj.amount = amount
        order_obj.save(force_update=True)
        ShoppingCart.objects.filter(user=request.session['customer_id']).delete()
        return redirect("/order")

def logout(request):
    try:
        del request.session['customer_id']
        del request.session['customer_name']
    except KeyError:
        messages.add_message(request, messages.ERROR, "Please login firstly.") 
    return redirect("/")
