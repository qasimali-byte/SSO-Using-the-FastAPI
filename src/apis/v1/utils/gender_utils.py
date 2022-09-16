def format_gender_selected_data(all_genders,selected_gender):
    for genders in all_genders:
        if selected_gender != None:
            if selected_gender.dr_iq_gender_id == genders["id"]:
                genders["is_selected"] = True
            else:
                genders["is_selected"] = False
        else:
            genders['is_selected'] = False

    return all_genders

def format_gender_selected_data_loged_in_area(selected_gender):
    
    gender_dict=dict({})
    if selected_gender==1:
        gender_dict['id'] = selected_gender
        gender_dict['name'] = 'male'
    
    if selected_gender==2 :
        gender_dict['id'] = selected_gender
        gender_dict['name'] = 'female'
        
    return gender_dict