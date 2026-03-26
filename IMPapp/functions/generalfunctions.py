

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
    """Handle DB helper response by redirecting or rendering error page.

    redirect_page may be a URL name (string) or a view function.
    The error template expects redirect_url to be a URL pattern name.
    """
    if response['status'] == 'success':
        return redirect(redirect_page)
    else:
        redirect_url = redirect_page if isinstance(redirect_page, str) else redirect_page.__name__
        return views.error(
            request,
            {
                'error': 'Error',
                'message': response['message'],
                'redirect_url': redirect_url,
            },
        )