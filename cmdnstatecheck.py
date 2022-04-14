from sermanager import serialmanager
import time
# import serial.tools.list_ports as sp
import sys


def main():
    
    com_port_info_cm = 'COM8'
    path_root = "CM>"
    cm_enter_key = "\r"
    # cm_fw_ver = "version"
    # cm_fw_ver_str = cm_fw_ver + cm_enter_key
    cm_cmd_movetoroot = "cd /"
    cm_cmd_movetoroot_str = cm_cmd_movetoroot + cm_enter_key
    
    # phrase_cur_fw_ver = "Revision:  0.4.0"
    # swupgdfilename = "hgj310v4_v0.4.0.img"
       
    phrase_cm_online_2nd = "CM is OPERATIONAL"
    phrase_tftpdnld_1st = "Loading from server"
    phrase_tftpdnld_2nd = "Storing to device"
    phrase_tftpdnld_end_1st = "we have reached end of file"
    phrase_tftpdnld_end_2nd = "Tftp transfer complete"
    phrase_filenvwrite_end = "NV write success"
    
    fwdnstat_list = [phrase_cm_online_2nd,
                     phrase_tftpdnld_1st,
                     phrase_tftpdnld_2nd,
                     phrase_tftpdnld_end_1st,
                     phrase_tftpdnld_end_2nd,
                     phrase_filenvwrite_end]
    
    print(len(fwdnstat_list))
    
    for phrase in fwdnstat_list:
        print(type(phrase))
        print(phrase)
    
    # buffer = bytes()
    
    sercon = serialmanager(com_port_info_cm)
    
    if sercon.check_comport(com_port_info_cm) == True:
        print(f'{com_port_info_cm} is a current avaiable port list.')
        pass
    else:
        sys.exit(f'{com_port_info_cm} is not an available port. Please check your com port is right.')
    
    try:
        ser = sercon.open_serial()  
        # 최초 연결 후 특별히 input, output에 buffer가 남아 없겠지만 혹시 모를 상황을 위해 buffer를 reset 시킴
        ser.reset_input_buffer()
        ser.reset_output_buffer()              
    except Exception as e:
        print(f'Exception has occurred with this reason: {e}')
        
    sercon.read_serialbuffer_fwdn(fwdnstat_list)
       
    pass


if __name__ == "__main__":
    
    main()
    pass