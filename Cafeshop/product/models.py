from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=255)
    count_order = models.IntegerField()

class Promotion(models.Model):
    s_date = models.DateField(auto_now=True)
    e_date = models.DateField(auto_now=True)
    promo_desc = models.TextField()
    promo_status = models.BooleanField(default=False)
class Reciept(models.Model):
    total_price = models.FloatField()
    date_time = models.DateTimeField(auto_now=True)
 
class Staff(models.Model):
    st_name = models.CharField(max_length=255)

class Queue_info(models.Model):
    date_time = models.DateTimeField(auto_now=True)


class Order(models.Model):
    
    TYPE_BUY = (
        ('Local_buy', 'Local buy'),
        ('Online_buy', 'Online buy')
    )
    
    TYPE_PAY = (
        ('Cash', 'Cash'),
        ('Credit', 'Credit')
    )

    order_type = models.CharField(max_length=255, choices=TYPE_BUY)
    Order_payment = models.CharField(max_length=255, choices=TYPE_PAY)
    date = models.DateTimeField(auto_now=True)
    promo_id = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    c_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    receipt_id = models.ForeignKey(Reciept, on_delete=models.CASCADE)
    queue = models.ForeignKey(Queue_info, on_delete=models.CASCADE)

class Drink_info(models.Model):
    
    DRINK_TYPE = (
        ('Coffee', 'Coffee'),
        ('Juice', 'Juice')
    )
    
    d_name = models.CharField(max_length=255)
    cost = models.IntegerField()
    drink_type = models.CharField(max_length=50, choices=DRINK_TYPE)

class Special(models.Model):

    SPECIAl_TYPE = (
        ('Coffee', 'Coffee'),
        ('Juice', 'Juice')
    )
    
    special_type = models.CharField(max_length=50, choices=SPECIAl_TYPE) 
       
class Order_list(models.Model):
    amount = models.IntegerField()
    unit_price = models.FloatField()
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    d_id = models.ForeignKey(Drink_info, on_delete=models.CASCADE)
    special_id = models.ForeignKey(Special, on_delete=models.CASCADE)   
    


class Fruit(models.Model):
    fruit_name = models.CharField( max_length=30)
    fruit_desc = models.CharField( max_length=50)

class Option(models.Model):
    option_name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    price = models.FloatField()


class Juice(models.Model):
    special_id = models.OneToOneField(Special, primary_key=True, on_delete=models.CASCADE)
    fruits = models.ManyToManyField(Fruit, through='Juice_fruit')
    options = models.ManyToManyField(Option, through='Juice_option')

class Juice_fruit(models.Model):
    juice = models.ForeignKey(Juice, on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Coffee_and_other(models.Model):
    
    COFFEE_TYPE = (
        ('Hot', 'Hot'),
        ('Iced', 'Iced'),
        ('Frappe', 'Frappe')
    )
    
    specials = models.OneToOneField(Special, on_delete=models.CASCADE, primary_key=True)
    coffee_type = models.CharField(max_length=50, choices=COFFEE_TYPE) 
    options = models.ManyToManyField(Option, through='Coffee_and_other_option')

class Coffee_and_other_option(models.Model):
    Coffee_and_other = models.ForeignKey(Coffee_and_other, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    amount = models.IntegerField()
    

class Juice_option(models.Model):
    juice = models.ForeignKey(Juice, on_delete=models.CASCADE)
    fruit = models.ForeignKey(Option, on_delete=models.CASCADE)
    amount = models.IntegerField()
















