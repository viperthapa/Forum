from .models import NormalUser,Question


def UserImage(request):
    users = NormalUser.objects.all()
    
    return {
        'users':users,
            
    }
    

    
    