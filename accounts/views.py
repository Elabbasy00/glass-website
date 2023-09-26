from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView
from django.contrib import messages
from .models import User, Address

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import UserProfileUpdate,AddNewAddress

# Create your views here.

def get_short_name(user):
        # The user is identified by their email address
        return user.email



#TODO: require Auth
def user_active(request):
    '''
            - get code from request 
            - check if the code exist in user model
            - activate user account
            - redirect to profile view
    '''
    if request.method == 'POST':
        code = request.POST.get('code')
        if code:
            pass

    pass

#TODO: require Auth
def resend_active_code(request):
    '''
        - generate 6 digit
        - update code in user model
        - send sms
        - redirect to inactive view
    '''
    pass

@login_required
def profile(request):
    user = get_object_or_404(User.objects.prefetch_related("address_set", "orderitem_set", "order_set"),id=request.user.id)
    if request.method == 'POST':
        type = request.POST.get('type')
        if type == 'user_info':
            user_info_form = UserProfileUpdate(request.POST, instance=request.user)
            if user_info_form.is_valid():
                    user_info_form.save()
                    messages.success(request, 'Your profile is updated successfully')
                    return redirect(to='accounts:profile')
            else:
                messages.error(request, user_info_form.errors)
                return redirect(to='accounts:profile')

        elif type == 'add_address':
            new_address_form = AddNewAddress(request.POST)
            if new_address_form.is_valid():
                obj = new_address_form.save(commit=False)
                obj.user = user
                default_adddress = user.address_set.filter(default=True)
                if default_adddress and obj.default:
                    default_adddress[0].default = False
                    default_adddress[0].save()
                obj.save()
                messages.success(request, 'New address added successfully')
                return redirect(to='accounts:profile')
            else:
                messages.error(request, new_address_form.errors)
                return redirect(to='accounts:profile')
    else:
        user_info_form = UserProfileUpdate(instance=request.user)
        new_address_form = AddNewAddress(instance=request.user)

    return render(request, 'account/profile.html', {"user": user, "info_form":user_info_form, "address_form": new_address_form })


@login_required
def delete_address(request, id):
        try:
            address = get_object_or_404(Address, id=id)  
            address.delete()
            messages.success(request, 'address deleted successfully')
            return redirect(to='accounts:profile')
        except Exception as e:
            messages.Error(request, e)
            return redirect(to='accounts:profile')

@login_required
def default_address(request, id):
        user = get_object_or_404(User.objects.prefetch_related("address_set"),id=request.user.id)
        address = get_object_or_404(Address, id=id)
        try:
            default_adddress = user.address_set.filter(default=True)
            if default_adddress:
                default_adddress[0].default = False
                default_adddress[0].save()
            address.default = True
            address.save()
            messages.success(request, 'address Update successfully')
            return redirect(to='accounts:profile')
        except Exception as e:
            print(e)
            messages.Error(request, e)
            return redirect(to='accounts:profile')
            

    