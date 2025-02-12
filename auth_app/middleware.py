from django.shortcuts import redirect



def auth(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated == False:
            return redirect('home')
        return view_function(request, *args, **kwargs)
    return wrapper
    
        
def guest(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return view_function(request, *args, **kwargs)
    return wrapper
            