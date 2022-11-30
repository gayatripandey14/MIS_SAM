# from smpp.models import UserDetails
from smpp.models import SmppUser
from testapp.models import AccountsSmppusers
from users.models import AccountsUser, ServicesServicedetail, ServicesServices
from .serializers import *



def check_if_parent(child_user, parent_user):
    if child_user == parent_user: return True 
    
    while child_user:
        if child_user == parent_user:
            print("child_user is a child of parent_user") 
            return True
        child_user = child_user.created_by
    print("not a child")
    return False
    


def get_master_routes(user):
    rtrn_routes = []

    # count = 1

    while user:
        # space = ' ' * count
        routes = ServicesServicedetail.objects.filter(created_by = user,expired=False)
        # print(f"{space}{user.user_type} created {len(routes)} routes.")
        rtrn_routes.extend(routes)

        # if user.created_by:
            # print(space, user.user_type, "CREATED BY ", user.created_by.id, user.created_by.email, user.created_by.user_type, sep=' -- ')      
        # else: print(f"{space}THIS IS YOUR SUPER ADMIN. [END OF LOOP]")
        
        user = user.created_by
        # count = count + 5
    
    # print(user)
    # print(f"[MASTER] found total {len(rtrn_routes)} routes for this user.\n\n")
    
    return rtrn_routes


def get_children_routes(user, count=1):
    # space = ' ' * count

    if user.user_type in ['User', "Reseller"]:
        # print(f"{space}{user.user_type} found. skipping")
        return []

    children = AccountsUser.objects.filter(created_by = user)
    # if children: print(f"{space}***found {len(children)} children for this user {user.user_type}***")

    rtrn_routes = []
    for i, child in enumerate(children):
        # print(f"{space}{i} --> gettings routes for child [{child.id} {child.user_type}]", end='-       \t')
        routes = ServicesServicedetail.objects.filter(created_by = child,expired=False)
        # print(f"[{len(routes)} routes]")
        rtrn_routes.extend(routes)
        rtrn_routes.extend(get_children_routes(child, count+5))

    return rtrn_routes


def get_childrens(user, count=1):
    space = ' ' * count


    children = AccountsUser.objects.filter(created_by = user)
    if children: print(f"{space}found {len(children)} children for this user {user.user_type}")

    rtrn_routes = []

    for i, child in enumerate(children):
        print(child)

        print(f"{space}{i} --> gettings routes for child [{child.email} {child.id} {child.user_type}]", end='-               \t')
        routes = AccountsSmppusers.objects.filter(assigned_to = child.id,delete=False)
        usernames = []
        for x in routes:
            username = SmppUser.objects.get(system_id=x.smpp_userdetails_id).system_id
            # usernames.append({username:child.email})
            usernames.append({"username":username,"account_user_email":child.email,"smpp_user_id":x.id})


        print(f"[{routes.count()} routes]")
        rtrn_routes.extend(usernames)
        rtrn_routes.extend(get_childrens(child, count+5))
    
    return rtrn_routes


def get_childrens_under_user(user, count=1):
    space = ' ' * count

    
    children = AccountsUser.objects.filter(created_by = user,is_active=True)
    if children: print(f"{space}found {len(children)} children for this user {user.user_type}")

    rtrn_routes = []
    for i, child in enumerate(children):
        
        rtrn_routes.append({'id':child.id,'email':child.email})
        rtrn_routes.extend(get_childrens_under_user(child, count+5))

    return rtrn_routes    