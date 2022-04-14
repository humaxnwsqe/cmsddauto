from serialmanager import SerialManager
from config import Config

import time
# import serial.tools.list_ports as sp
import sys


class CMMacInfoThroughSerial():    
    
    def __init__(self, port = None):
        
        if port == None:
            print("CM console port info was not written in your code. Please check that data in the code.")
            return
        
        if str(type(port)) == "<class 'str'>":
            self.port = port
            self.sercon = SerialManager(self.port)
            self.buffer = bytes()
            
            print("CMMacInfoThroughSerial Class initialization has finished successfully.")
            try:
                self.ser = self.sercon.open_serial()
                print(f"CM serial: {self.port} has opened successfully.")
                self.ser.reset_input_buffer()
                self.ser.reset_output_buffer()  
            except Exception as e:
                print(f'Exception has occurred with this reason: {e}')
        else:
            print("Used cm console port data is not a type of string. Please check the port value in the code.")
            return   
    
    def __del__(self):
        try:
            self.sercon.close_serial(self.port)
            print("CMMACInfoThroughSerial Class instance has removed.")
        except Exception as e:
            print(f'Exception has occurred with this reason during close serial: {e}')  
        pass
    
    def get_CM_Mac_Info(self):        
        
        cm_info_strs = []
        
        # CM root path 상태인지 확인하고 root path가 아닐 경우에는 root path로 이동한다.
        for i in range(0, 10):
            self.ser.reset_output_buffer()
            time.sleep(0.5)       
            self.ser.write(Config.KEY_ENTER.encode())  
            self.ser.flush()
            time.sleep(0.5)
            
            buffer = self.sercon.read_serialbuffer(self.buffer)
            
            if Config.CM_PATH_CM in buffer.decode():
                print("The current CM console path is a root state. Let's move to the next step.")
                self.ser.reset_output_buffer()
                buffer = bytes()
                break
            else:
                print("The current CM console path is not a root state.")
                buffer = bytes()
                
                time.sleep(0.5)       
                self.ser.write(Config.CM_CMD_MOVETOROOT_STR.encode())  
                self.ser.flush()
                time.sleep(0.5)  

        
        for i in range(0,10):
            self.ser.reset_output_buffer()
            time.sleep(0.5)       
            self.ser.write(Config.KEY_ENTER.encode())  
            self.ser.flush()
            time.sleep(0.5)     
            self.ser.write(Config.CM_CMD_MOVETOCONSOLE_STR.encode())  
            self.ser.flush()
            time.sleep(0.5)
            
            buffer = self.sercon.read_serialbuffer(buffer)
            
            if Config.CM_PATH_CM_CONSOLE in buffer.decode():
                print("To move to console path is OK.")
                time.sleep(0.5)       
                self.ser.write(Config.CM_CMD_SHOWIP_STR.encode())
                self.ser.flush()
                time.sleep(0.5)
                buffer = bytes()
                buffer = self.sercon.read_serialbuffer(buffer)
                strings = buffer.decode().split()
                i = 0
                j = 0
                # cm_info_strs = []
                print(strings)
                
                for part in strings:                
                    if part == "1":
                        print(f"{i}   :  {part}")
                        cm_info_strs.append(part)
                        j = i
                    elif j != 0 and (j + 1) == i:
                        print(f"{i}   :  {part}")
                        cm_info_strs.append(part)
                    elif j != 0 and (j + 2) == i:
                        print(f"{i}   :  {part}")
                        cm_info_strs.append(part)
                        # print(cm_info_strs)
                        break
                    i = i + 1
                break
            else:
                print("The current path is not a CM/CM_Console>. Please retry.")
                pass
        cm_mac = cm_info_strs[2]
        return cm_mac

# def main():    
#     cmmacinfo = CMMacInfoThroughSerial('com7')    
#     print(cmmacinfo.get_CM_Mac_Info())    
#     # comport = 'com7'    
#     # print(type(comport))    
#     pass

# if __name__ == '__main__':      
#     main()       
#     pass
