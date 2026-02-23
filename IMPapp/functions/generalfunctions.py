

# 
# validate user can complete action
#
from urllib import request
from django.shortcuts import redirect
from IMPapp import views


def validateUserAuthorisation(request, permission_codename):
    # check group permissions
    for group in request.user.groups.all():
        for perm in group.permissions.all():
            # if the permission matches
            if perm.codename == permission_codename:
                # user is authorised
                return True
    # check user permissions
    for perm in request.user.user_permissions.all():
        # if the permission matches
        if perm.codename == permission_codename:
            # user is authorised
            return True
    # user is NOT authorised
    return False


#
#
#
def handleResponse(request, response, redirect_page):
    if response['status'] == 'success':
        return redirect(redirect_page)
    else:
        return views.error(request, {'error' : 'Error', 'message': response['message'], 'redirect_url': redirect_page})