from django  import forms
from .models import rentals,product,category,confirmorder


class rentalsform(forms.ModelForm):
    class Meta:
        model = rentals
        fields = "__all__"
        exclude = ('user',)
        
class productform(forms.ModelForm):
    class Meta:
        model = product
        fields = "__all__"
        exclude = ('user',)
        
class categoryform(forms.ModelForm):
    class Meta:
        model = category
        fields = "__all__"
        exclude = ('user',)
        
class confirmorderform(forms.ModelForm):
    class Meta:
        model = confirmorder
        fields = "__all__"
        exclude = ('user',)     
        

    
    
    
    
    
    
    
    
    
    
    