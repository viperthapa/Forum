from django.dispatch import Signal

###    create a signal when a someone comment in particular questions

 
new_comment = Signal(providing_args=["job", "subscriber"])