# from sermanager import SerialManager
import time
# import serial.tools.list_ports as sp
import sys
from config import Config


# def main():
class SWVersionCheckingInCM(): # SWVersionCheckingInCM
    
    # com_port_info_cm = 'COM8'
    # path_root = "CM>"
    # cm_enter_key = "\r"
    # cm_fw_ver = "version"
    # cm_fw_ver_str = cm_fw_ver + cm_enter_key
    # cm_cmd_movetoroot = "cd /"
    # cm_cmd_movetoroot_str = cm_cmd_movetoroot + cm_enter_key
    
    # phrase_cur_fw_ver = "Revision:  0.3.7"
    # swupgdfilename = "hgj310v4_v0.4.0.img"
    
    # Initialization of class cmswvercheck
    def __init__(self):
        self.buffer = bytes()
        # self.path_root = "CM>"
        self.path_root = Config.CM_PATH_CM
        # self.cm_enter_key = "\r"
        self.cm_enter_key = Config.KEY_ENTER
        # self.cm_fw_ver = "version"
        self.cm_fw_ver = Config.CM_FW_VER_EXPRESSION
        self.cm_fw_ver_str = self.cm_fw_ver + self.cm_enter_key
        # self.cm_cmd_movetoroot = "cd /"
        self.cm_cmd_movetoroot = Config.CM_CMD_MOVETOROOT
        self.cm_cmd_movetoroot_str = self.cm_cmd_movetoroot + self.cm_enter_key
        # self.phrase_cur_fw_ver = curfwver
        # self.pharse_revision = "Revision:"
        self.pharse_revision = Config.CM_FW_REVISION_EXPRESSION
        # pass
    
    # CM console에서 sw version 정보를 확인하고 버전 정보를 return 한다.
    def get_swver_frm_cm(self, serial, serialmanager):
        
        ser = serial
        sercon = serialmanager
        tmp_ver = ""        
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
                print(f"The current CM console path is '{self.path_root}' state. Let's check current f/w version.")
                ser.reset_output_buffer()
                self.buffer = bytes()
                
                ser.write(self.cm_fw_ver_str.encode())
                ser.flush()
                time.sleep(0.5)
                
                self.buffer = sercon.read_serialbuffer(self.buffer)
                
                lines = self.buffer.decode().splitlines()
                
                for line in lines:
                    # print(type(line))
                    # if self.phrase_cur_fw_ver in line:
                    if self.pharse_revision in line:                    
                        print(str(line))
                        tmp_ver = str(line)
                        bflag = True
                        print(f"The current version is '{tmp_ver}'.")
                        break  
                    
                if bflag == True:
                    break            
                # if self.phrase_cur_fw_ver in self.buffer.decode():
                #     print(f"The current version is '{self.phrase_cur_fw_ver}'.")
                #     break  
                # else:
                #     print(f"The current version is NOT '{self.phrase_cur_fw_ver}' Please try to upgrade new f/w if it is required.")
                #     break
                            
                
            else:
                print(f"The current CM console path is not '{self.path_root}' state. The path will be moved to '{self.path_root}'.")
                self.buffer = bytes()
                
                time.sleep(0.5)       
                ser.write(self.cm_cmd_movetoroot_str.encode())              
                # ser.write(cm_cmd_movetocm_str.encode())
                ser.flush()
                time.sleep(0.5) 
        
        if tmp_ver != "":
            noblank_ver = tmp_ver.replace(" ", "")
            items = noblank_ver.split(':')
            print(f"items type is '{type(items)}' and the length of items is '{len(items)}'")
            for i in range(0, len(items)):
                print(f"{i} : {items[i]}")
                if i == 1:
                    tmp_ver = items[i]
            
            pass
                
        return tmp_ver
            
    
    # pass


# if __name__ == "__main__":
    
#     main()
#     pass