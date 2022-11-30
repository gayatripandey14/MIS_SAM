from users.models import AccountsUser
from testapp.models import AccountsSmscroutes as SmppSmscRoutes


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

    count = 1

    while user:
        space = ' ' * count
        routes = SmppSmscRoutes.objects.filter(user = user.id)
        print(f"{space}{user.user_type} created {len(routes)} routes.")
        rtrn_routes.extend(routes)

        if user.created_by:
            print(space, user.user_type, "CREATED BY ", user.created_by.id, user.created_by.email, user.created_by.user_type, sep=' -- ')      
        else: print(f"{space}THIS IS YOUR SUPER ADMIN. [END OF LOOP]")
        
        user = user.created_by
        count = count + 5
    
    print(f"[MASTER] found total {len(rtrn_routes)} routes for this user.\n\n")
    
    return rtrn_routes


def get_children_routes(user, count=1):
    space = ' ' * count

    if user.user_type in ['User', "Reseller"]:
        print(f"{space}{user.user_type} found. skipping")
        return []

    children = AccountsUser.objects.filter(created_by = user)
    if children: print(f"{space}***found {len(children)} children for this user {user.user_type}***")

    rtrn_routes = []
    for i, child in enumerate(children):
        print(f"{space}{i} --> gettings routes for child [{child.id} {child.user_type}]", end='-               \t')
        routes = SmppSmscRoutes.objects.filter(user = child.id)
        print(f"[{len(routes)} routes]")
        rtrn_routes.extend(routes)
        rtrn_routes.extend(get_children_routes(child, count+5))

    return rtrn_routes
