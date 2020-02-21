from django.contrib import admin
from datetime import datetime
from django.core.mail import send_mail
from jinja2 import Template

from .models import Category, Item, ItemOption, ItemExtra, Toppings, Order, Customer
from .models import IndexShelf, Contact, Customer
from .constant import ORDER_COMPLETED_MAIL_TEMPLATE

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('name', 'description')

class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    list_display = ('username', 'first_name', "last_name", "email")

    def get_form(self, request, obj=None, **kwargs):
        return super().get_form(request, obj=obj, fields=['username', 'first_name', "last_name", "email"])

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('name', 'description', 'category')

class ItemOptionAdmin(admin.ModelAdmin):
    model = ItemOption
    list_display = ('name', 'item', 'price')

class ItemExtraAdmin(admin.ModelAdmin):
    model = ItemExtra
    list_display = ('item_option', 'topping', 'cost')

class ToppingsAdmin(admin.ModelAdmin):
    model = Toppings
    list_display = ('name',)

class IndexShelfAdmin(admin.ModelAdmin):
    model = IndexShelf
    list_display = ('title',)

class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ('title', 'email', 'address', 'phone')

class OrderAdmin(admin.ModelAdmin):
    model = Order 
    list_display = ('order_num', "status") 
    change_form_template = "admin/order_change_form.html"
    actions = None

    def get_readonly_fields(self, request, obj=None):
        return ['amount', 'created_by', 'updated_by']

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user.username
        obj.update_time = datetime.now()
        obj.save()
        if obj.status == "completed":
            customer = obj.created_by
            send_mail("Your order num {0} is completed.".format(obj.order_num),
            "", request.user.email, [customer.email],
            html_message=Template(ORDER_COMPLETED_MAIL_TEMPLATE, autoescape=True).render({
                "last_name": customer.last_name,
                "first_name": customer.first_name,
                "order_num": obj.order_num,
                "admin_name": request.user.username,
                "amount": obj.amount,
                "order_details": obj.get_item_detail()
            }))

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = {}
        extra_context["order_details"] = Order.objects.get(pk=object_id).get_item_detail()
        if Order.objects.get(pk=object_id).status == "completed":
            extra_context["show_save"] = False
            extra_context["show_save_and_continue"] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemOption, ItemOptionAdmin)
admin.site.register(ItemExtra, ItemExtraAdmin)
admin.site.register(Toppings, ToppingsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(IndexShelf, IndexShelfAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Customer, CustomerAdmin)