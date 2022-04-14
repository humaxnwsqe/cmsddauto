import re

class DataHandler():
    
    def __init__(self):
        pass
    
    def get_swver_frm_filename(self, swfilename):
        
        tmp_filename = swfilename
        
        model_id = "None"
        sw_ver = "None"
        sep_filename_list = None        
        
        if isinstance(tmp_filename, str):
            print(f"Used parameter's value '{tmp_filename}' is a string type.")
            
            # "hgj310v4_v0.4.0.img"
            sep_filename_list = tmp_filename.split('_')
            
            for item in sep_filename_list:
                print(item)
            
            model_id = sep_filename_list[0]
            
            if model_id == "hgj310v4":
                for item in sep_filename_list[1].partition('.img'):
                    if item != ".img" and item != '':
                                                
                        print(f"item type is '{type(item)}' and the value is '{item}'")
                        list = item.partition('v')
                        for sub_item in list:
                            if sub_item != 'v':
                                print(sub_item)
                                sw_ver = sub_item
                            # sw_ver = item
                        
                        
            else:
                print(f"The current model is {model_id}. It will be handle in the next time.")
        else:
            print(f"{tmp_filename} is not a string type. Please check the used parameter.")
            
            # print(tmp_filename.partition('_v'))
            
            # for cur in re.split('[_]', tmp_filename):
            #     print(cur)
                
        return sw_ver 
            
        
    
    # pass