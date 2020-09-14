from .models import NormalUser,Question


def UserImage(request):
    users = NormalUser.objects.all()
    # education = Question.objects.filter(category = "education")[:4]
    # sports = Question.objects.filter(category = "sports")[:4]
    # print("sports = ",sports)
    # politics = Question.objects.filter(category = "politics")[:4]
    # fashion_and_style = Question.objects.filter(category = "fashion and style")[:4]
    # Health = Question.objects.filter(category = "Health")[:4]
    # it = Question.objects.filter(category = "Information and technology")[:4]
    
    return {
        'users':users,
        # 'education':education, 
        # 'sports':sports,
        # 'politics':politics,
        # 'fashion_and_style':fashion_and_style,
        # 'Health':Health,
        # 'it':it,
            
    }
    

    
    