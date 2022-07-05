def format_practices_edit_user_data(practices_of_userid, practices_of_selected_user_id):
    regions_list = {}
    regions = {}
    practices_child_dict = {}

    for practices_child, practices_parent in practices_of_userid:

        ## create parent regions for practices
        if practices_parent == None:

            ## check whether already parent exsists or not 
            ## if parent exsists then we don't want to create parent again
            if regions_list.get(practices_child.id) == None:
                regions['id'] = practices_child.id
                regions['name'] = practices_child.name
                regions['practices'] = []

                for practices_child2, practices_parent2 in practices_of_selected_user_id:
                    if practices_child.id == practices_child2.id:
                        regions['is_selected'] = True
                        break
                else:
                    regions['is_selected'] = False
                ## creating a region for practices in unique practices id list
                regions_list[regions['id']] = dict(regions)


        elif practices_parent != None:
            regions['id'] = practices_parent.id
            regions['name'] = practices_parent.name
            
            ## empty practices created when the regions_list['id'] does not contain practices key:
            if regions_list.get(practices_parent.id) == None:
                for practices_child2, practices_parent2 in practices_of_selected_user_id:
                    if practices_parent2 != None:
                        if practices_parent.id == practices_parent2.id:
                            regions['is_selected'] = True
                            break
                else:
                    regions['is_selected'] = False

                regions['practices'] = []
                ## creating a region for practices in unique practices id list
                regions_list[regions['id']] = dict(regions)

            

            ## create child practices for regions
            practices_child_dict['id'] = practices_child.id
            practices_child_dict['name'] = practices_child.name
            for practices_child2, practices_parent2 in practices_of_selected_user_id:
                    if practices_child.id == practices_child2.id:
                        practices_child_dict['is_selected'] = True
                        break
            else:
                practices_child_dict['is_selected'] = False

            regions_list[regions['id']]['practices'].append(dict(practices_child_dict))

    

    regions_list = [i for i in regions_list.values()]
    return regions_list