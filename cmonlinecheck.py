from sermanager import serialmanager
import time
# import serial.tools.list_ports as sp
import sys
from config import Config

def main():
    
    com_port_info_cm = 'COM8'
    path_con_cm = "CM/CM_Console/cm>"
    cm_enter_key = "\r"
    cm_cmd_onlinestate = "show status"
    cm_cmd_onlinestate_str = cm_cmd_onlinestate + cm_enter_key
    cm_cmd_movetoroot = "cd /"
    cm_cmd_movetoroot_str = cm_cmd_movetoroot + cm_enter_key
    cm_cmd_movetocm = "cd Con/cm"
    cm_cmd_movetocm_str = cm_cmd_movetocm + cm_enter_key
    
    phrase_cm_online = "Docsis Registration Status: Operational"
    phrase_cm_offline = "Docsis Registration Status: NotSynchronized"
    
    buffer = bytes()
    
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
    
    for i in range(0, 10):
        ser.reset_output_buffer()
        time.sleep(0.5)       
        ser.write(cm_enter_key.encode())  
        ser.flush()
        time.sleep(0.5)
                
        buffer = sercon.read_serialbuffer(buffer)
        
        if path_con_cm in buffer.decode():
            print(f"The current CM console path is '{path_con_cm}' state. Let's check current CM state which is 'Operational' or 'NotSynchronized.")
            ser.reset_output_buffer()
            buffer = bytes()
            
            ser.write(cm_cmd_onlinestate_str.encode())
            ser.flush()
            time.sleep(0.5)
            
            buffer = sercon.read_serialbuffer(buffer)
                        
            if phrase_cm_online in buffer.decode():
                print("The current CM state is online(Operational).")
                break
            elif phrase_cm_offline in buffer.decode():
                print("The current CM state is offline(NotSynchronized).")
            else:
                print("The current CM state is neither online nor offline. Please check your CM DUT which is working well or not.")               
            
        else:
            print(f"The current CM console path is not '{path_con_cm}' state. The path will be moved to '{path_con_cm}'.")
            buffer = bytes()
            
            time.sleep(0.5)       
            ser.write(cm_cmd_movetoroot_str.encode())              
            ser.write(cm_cmd_movetocm_str.encode())
            ser.flush()
            time.sleep(0.5) 
            
    
    pass


if __name__ == "__main__":
    
    main()
    pass