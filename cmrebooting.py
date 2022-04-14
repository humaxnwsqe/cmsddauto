from serialmanager import SerialManager
import time
# import serial.tools.list_ports as sp
import sys
from config import Config

# def main():

class CMRebooting():
    
    def __init__(self):    
        self.buffer = bytes()    
        # com_port_info_cm = 'COM8'
        # self.path_root = "CM>"
        self.path_root = Config.CM_PATH_CM
        # self.cm_enter_key = "\r"
        self.cm_enter_key = Config.KEY_ENTER
        # cm_cmd_reset = "reset"
        cm_cmd_reset = Config.CM_CMD_RESET
        self.cm_cmd_reset_str = cm_cmd_reset + self.cm_enter_key
        # cm_cmd_movetoroot = "cd /"
        cm_cmd_movetoroot = Config.CM_CMD_MOVETOROOT
        self.cm_cmd_movetoroot_str = cm_cmd_movetoroot + self.cm_enter_key        
        # self.phrase_cm_reset_done = "Rebooting now so we don't trip all over ourselves"
        self.phrase_cm_reset_done = Config.CM_RESET_DONE_MSG
        
    
    # sercon = serialmanager(com_port_info_cm)
    
    # if sercon.check_comport(com_port_info_cm) == True:
    #     print(f'{com_port_info_cm} is a current avaiable port list.')
    #     pass
    # else:
    #     sys.exit(f'{com_port_info_cm} is not an available port. Please check your com port is right.')
    
    # try:
    #     ser = sercon.open_serial()  
    #     # 최초 연결 후 특별히 input, output에 buffer가 남아 없겠지만 혹시 모를 상황을 위해 buffer를 reset 시킴
    #     ser.reset_input_buffer()
    #     ser.reset_output_buffer()              
    # except Exception as e:
    #     print(f'Exception has occurred with this reason: {e}')
    
    def cm_do_reset(self, serial, serialmanager):
        
        ser = serial
        sercon = serialmanager
        self.buffer = bytes() 
        bflag = False
        
    
        for i in range(0, 10):
            ser.reset_output_buffer()
            time.sleep(0.5)       
            ser.write(self.cm_enter_key.encode())  
            ser.flush()
            time.sleep(0.5)
            
            self.buffer = sercon.read_serialbuffer(self.buffer)
            
            if self.path_root in self.buffer.decode():
                print(f"The current CM console path is '{self.path_root}'. Let's reboot this DUT.")
                ser.reset_output_buffer()
                self.buffer = bytes()
                ser.write(self.cm_cmd_reset_str.encode())
                time.sleep(0.5)
                self.buffer = sercon.read_serialbuffer(self.buffer)
                print(self.buffer.decode())
                if self.phrase_cm_reset_done in self.buffer.decode():
                    print("Reboot command has done successfully!")
                    bflag = True
                break
            else:
                print(f"The current CM console path is not '{self.path_root}'.")
                self.buffer = bytes()
                
                time.sleep(0.5)       
                ser.write(self.cm_cmd_movetoroot_str.encode())  
                ser.flush()
                time.sleep(0.5) 
        
        return bflag
        pass


# if __name__ == "__main__":
    
#     main()
#     pass