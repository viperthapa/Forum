from .models import NormalUser


def UserImage(request):
    users = NormalUser.objects.all()
    return {
        'users':users
    }
    

    
    