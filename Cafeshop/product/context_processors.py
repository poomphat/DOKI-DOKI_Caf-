from product.models import Promotion

def pro_to_base(request):    
    promotions = Promotion.objects.all()    
    return {'Promotion': promotions}