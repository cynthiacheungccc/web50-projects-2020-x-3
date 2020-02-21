from django.db import models
import uuid
from pizza.settings import INDEX_SHELF_IMAGE_PATH


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Toppings(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    extra_limit = models.IntegerField()

    def __str__(self):
        return "{0} ({1})".format(self.name, self.category)

class ItemOption(models.Model):
    name = models.CharField(max_length=100)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.item)

class ItemExtra(models.Model):
    item_option = models.ForeignKey(ItemOption, on_delete=models.CASCADE)
    topping = models.ForeignKey(Toppings, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    def __str__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

class ShoppingCart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item_option = models.ForeignKey(ItemOption, on_delete=models.CASCADE)
    item_extra = models.ManyToManyField(ItemExtra)
    item_num = models.IntegerField(default=1)

class Order(models.Model):
    status = models.CharField(max_length=20, choices=[("new", "New"), ("pending", "Pending"), ("completed", "Completed")], default="new")
    order_num = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(Customer, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    update_time = models.DateTimeField(auto_now=True)

    def get_item_detail(self):
        order_items = OrderItem.objects.filter(order=self.pk)
        extra_items = [ item for item in order_items if item.item_type == "extra" ]
        option_items = [ item for item in order_items if item.item_type == "option"] 
        detail = []
        for item in option_items:
            option = ItemOption.objects.get(pk=item.item_id)
            sub_detail = {"name": option.item.name, "option": option.name, "price": item.item_cost, "num": item.item_num}
            sub_detail["extras"] = []
            for order_item in extra_items:
                extra = ItemExtra.objects.get(pk=order_item.item_id)
                if extra.item_option == option:
                    sub_detail["extras"].append({
                        "name": extra.topping.name,
                        "num": order_item.item_num,
                        "cost": order_item.item_cost
                    })
            detail.append(sub_detail)
        return detail

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=20, choices=[("option", "Option"), ("extra", "Extra")], default="option")
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)
    item_id = models.IntegerField()
    item_num = models.IntegerField(default=1)


class IndexShelf(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to=INDEX_SHELF_IMAGE_PATH)

    def __str__(self):
        return self.title
    

class Contact(models.Model):
    title = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.title
    


