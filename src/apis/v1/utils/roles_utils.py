
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
    selected_roles = list([dict({'id':int, 'name':str})])
    if selected_role is None:
        return ['']
    else:
        selected_roles[0]['id']=selected_role[1].id
        selected_roles[0]['name']=selected_role[1].name
        if selected_role[2] != None:
            selected_roles[0]['sub_role']=list([dict({'id':selected_role[2].id,'name':selected_role[2].name})])
        else:
            selected_roles[0]['sub_role']=['']
    return selected_roles           
