def ip_family_detection_dictionary(ip_family:any=None,is_successful:bool=True)->dict:
    return {"ip_family":ip_family,"is_successful":is_successful}

def establish_connection_status_dictionary(hostname:str,port:int,is_successful:bool=False)->dict:
    return {"hostname":hostname,"port":int,"is_successful":is_successful}

