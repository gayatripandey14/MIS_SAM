from smpp.models import SmppUser
from testapp.models import AccountsSmppusers
from users.models import AccountsUser, ServicesServicedetail, ServicesServices



def get_routes(user,route, count=1):
    space = ' ' * count


    children = AccountsUser.objects.filter(created_by = user,is_active=True)
    # if children: print(f"{space}found {len(children)} children for this user {user.user_type}")

    rtrn_routes = []

    for i, child in enumerate(children):
        

        # print(f"{space}{i} --> gettings routes for child [{child.email} {child.id} {child.user_type}]", end='-               \t')
        routes = AccountsSmppusers.objects.filter(assigned_to = child.id,route=route,delete=False)
        usernames = []
        for x in routes:
            username = SmppUser.objects.get(system_id=x.smpp_userdetails_id).system_id
            usernames.append({"username":username})
        rtrn_routes.extend(usernames)
        rtrn_routes.extend(get_routes(child, count+5))
    
    return rtrn_routes