from product.models import Promotion
import datetime
def pro_to_base(request):    
    promotions = Promotion.objects.all()
    for promotion in promotions:
        #if promotion.e_date < datetime.date.today():
        #    promotion.promo_status = False
        #    promotion.save()

        #if promotion.s_date > datetime.date.today():
        #    promotion.promo_status = False
        #    promotion.save()
        
        if promotion.s_date < datetime.date.today() and promotion.e_date > datetime.date.today():
            promotion.promo_status = True
            promotion.save()
        else :
            promotion.promo_status = False
            promotion.save()
            
            
    promotions = promotions.filter(promo_status = True)   
    return {'Promotion': promotions}