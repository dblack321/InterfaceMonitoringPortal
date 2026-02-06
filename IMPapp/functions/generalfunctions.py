

# 
# validate user can complete action
#
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