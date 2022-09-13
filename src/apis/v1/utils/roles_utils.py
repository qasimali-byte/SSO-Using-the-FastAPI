
def format_roles_with_selected_roles(all_app_roles, selected_roles):
    if selected_roles is None:
        selected_roles = (None,None,None)

    for all_roles in all_app_roles:
        if selected_roles[1] != None:
            if all_roles['id'] == selected_roles[1].id:
                all_roles['is_selected'] = True
            else:
                all_roles['is_selected'] = False
        else:
            all_roles['is_selected'] = False
        
        for sub_roles in all_roles['sub_roles']:
            if selected_roles[2] != None:
                if sub_roles['id'] == selected_roles[2].id:
                    sub_roles['is_selected'] = True
                else:
                    sub_roles['is_selected'] = False
            else:
                sub_roles['is_selected'] = False

    return all_app_roles

def format_loged_in_user_role(selected_role):
    selected_roles = dict({'id':int, 'name':str})
    if selected_role is None:
        return None
    else:
        selected_roles['id']=selected_role[1].id
        selected_roles['name']=selected_role[1].name
        if selected_role[2] != None:
            selected_roles['sub_role']=dict({'id':selected_role[2].id,'name':selected_role[2].name})
        else:
            selected_roles['sub_role']=None
    return selected_roles           
