from .models import NormalUser,Category


def UserImage(request):
    users = NormalUser.objects.all()
    Categorys = Category.objects.all()
    
    return {
        'users':users,
        'Categorys':Categorys
    }
    

    
    