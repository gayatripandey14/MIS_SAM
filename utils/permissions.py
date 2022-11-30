
from email import message
from rest_framework_simplejwt import exceptions
from rest_framework.permissions import BasePermission
from rest_framework import HTTP_HEADER_ENCODING, authentication
from users.models import AccountsUser
from jose import jwt,JWTError
from core.settings import SIMPLE_JWT



class IsReseller(BasePermission):
    """
    Check if user is a Reseller.
    """

    message = "User doesn't have permissions"

    def has_permission(self, request, view):
        return request.user.user_type =="Reseller"

    

class IsResellerAdmin(BasePermission):
    """
    Reseller or admin.
    """

    message = "User doesn't have permissions"

    def has_permission(self, request, view):
        return request.user.user_type =="Reseller" or request.user.user_type =="Admin"



class IsResellerAdminSuperAdmin(BasePermission):
    """
    Reseller or admin or superadmin.
    """

    message = "User doesn't have permissions"

    def has_permission(self, request, view):
        return request.user.user_type =="Reseller" or request.user.user_type =="Admin" or request.user.user_type == "Super Admin"


class AdminSuperAdmin(BasePermission):
    """
    Admin or superadmin.
    """

    message = "User doesn't have permissions"

    def has_permission(self, request, view):
        return  request.user.user_type =="Admin" or request.user.user_type == "Super Admin"


class IsAdminSuperAdminAgent(BasePermission):
    message = "User doesn't have permissions"

    def has_permission(self, request, view):
        return  request.user.user_type =="Admin" or request.user.user_type == "Super Admin" or request.user.user_type == "Agent"


class IsSuperAdmin(BasePermission):
    """
    Super admin.
    """

    message = "User doesn't have permissions"

    def has_permission(self, request, view):
        return  request.user.user_type =="Super Admin"

class IsAuthenticated(BasePermission):

    message = "User doesn't have permissions"

    def has_permission(self, request, view):
        print(request,"----")
        return True
        return request.user.is_active ==True

class IsUserActive(BasePermission):
    """
    User is active or not
    """

    message = "User is not active"

    def has_permission(self, request, view):
        return request.user.is_active ==True


class JWTAuthentication(authentication.BaseAuthentication):

    """
    Simple token based authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "Token ".  For example:
    Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def authenticate(self, request):
        print(request,"auth")
        try:
            auth = self.authenticate_header(request).split()

            if not auth or auth[0].lower() != 'bearer':
                return None
        except:return None

        # token = exceptions.AuthenticationFailed(msg)
        token = auth[1]
        # try:
        #     token = auth[1].decode()
        # except UnicodeError:
        #     msg = _('Invalid token header. Token string should not contain invalid characters.')
        #     raise exceptions.AuthenticationFailed(msg)
        usr,payload = self.authenticate_credentials(token)
        
        return usr,token

    def authenticate_credentials(self, payload):
        print(payload,"cred")

    
        payload = jwt.decode(payload,SIMPLE_JWT['SIGNING_KEY'],algorithms=SIMPLE_JWT['ALGORITHM'])
        user_id = payload['user_id']


        try:
            usr = AccountsUser.objects.get(id=user_id)
        except Exception as e:
            print(e)
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not usr.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))

        # if expiry < datetime.date.today():
        #     raise exceptions.AuthenticationFailed(_('Token Expired.'))
        print(usr,"--------")
        return usr,payload
        return (usr, payload)

    def authenticate_header(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        return token