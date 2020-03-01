from django.shortcuts import redirect


def method_dectect(function):
    def wrap(request, *arg, **kwargs):
        print("dectect method: ", request.method)
        if request.method == 'POST':
            return function(request, *arg, **kwargs)
        else:
            return redirect('/')

    return wrap
