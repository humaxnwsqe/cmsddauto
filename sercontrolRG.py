from serialmanager import SerialManager
import time
import sys

global com_port_info_rg

def main():
    
    # 변수들
    global com_port_info_rg
    com_port_info_rg = 'COM7' 
    rg_enter_key = "\r"
    rg_newline = "\n"
    rg_login_ID = "root"
    rg_login_ID_str = rg_login_ID + rg_enter_key
    # rg_login_PW = "humax@!0416"
    rg_login_PW = "hmxosync"
    rg_login_PW_str = rg_login_PW + rg_enter_key
    cm_console_open_cmd = "snmpset -v2c -c private 172.31.255.45 1.3.6.1.4.1.4413.2.2.2.1.9.1.2.1.0 i 2"
    cm_console_open_cmd_str = cm_console_open_cmd + "\r\n"
    rg_logout_cmd = "exit"
    rg_logout_cmd_str = rg_logout_cmd + rg_enter_key
    
    blogin = False
    
    buffer = bytes()
        
    # 우선 serial console 연결을 위한 serialmanager class를 불러옴
    sercon = SerialManager(com_port_info_rg)
    
    # 우리가 연결 시도하려는 com port가 현재 컴퓨터 시스템 상에서 유효한 port들(리스트)인지 확인하는 과정. 만약 유요하지 않은 port로 값이 주어진 상태라면 재 확인 후 유효한 port 값을 입력해야 함
    if sercon.check_comport(com_port_info_rg) == True:
        print(f'{com_port_info_rg} is a current avaiable port list.')
        pass
    else:
        sys.exit(f'{com_port_info_rg} is not an available port. Please check your com port is right.')
        
    # (1) RG serial console 연결 시도를 위해 주어진 serial 포트 정보로 serial console 연결 시도 
    try:
        ser = sercon.open_serial()  
        # 최초 연결 후 특별히 input, output에 buffer가 남아 없겠지만 혹시 모를 상황을 위해 buffer를 reset 시킴
        ser.reset_input_buffer()
        ser.reset_output_buffer()  
        #ser = open_serial(com_port_info_rg)            
    except Exception as e:
        print(f'Exception has occurred with this reason during open serial: {e}')
        #raise RuntimeError('Exception has occurred with this reason') from e
        
    #while True:    
    for i in range(0, 10):
        
        # (2) 현재 RG console 상태, 즉 login 전/후 상태를 확인를 확인하기 위해 Enter key에 준하는 값을 write 하고 buffer를 읽어 온다.
        #ser.reset_input_buffer()
        
        time.sleep(0.5)       
        ser.write(rg_enter_key.encode())  
        ser.flush()
        time.sleep(0.5)
        # print(str(ser.read(200)))  
        
        
        # buffer = bytes()
        # buffer = sercon.read_serialbuffer(ser, buffer)
        buffer = sercon.read_serialbuffer(buffer)
        
        
        if "Docsis-Gateway login" in buffer.decode():
            print("Start for RG login is ready.")
            break
        elif "root@Docsis-Gateway:~#" in buffer.decode():
            print("RG console is already login state.")
            break
        
    # (3) (2)에서 Enter key 입력 후 console 상에서 출력 내용을 확인 해 RG console login이 필요한 상태인지 확인한다.
    
    for i in range(0, 10):
        # (3-1) RG console login이 필요할 경우, RG ID, PW를 입력한다. 
        
        if "Docsis-Gateway login" in buffer.decode() and blogin == False:
            print("RG Login start!")
                        
            time.sleep(0.5)
            print("Entering RG console ID")
            ser.write(rg_login_ID_str.encode())
            ser.flush()
            time.sleep(0.5)
            print("Entering RG console PW")
            ser.write(rg_login_PW_str.encode()) 
            ser.flush()
            time.sleep(0.5)            
            print("Entering 'Enter key' to ensure 'root@Docsis-Gateway:~#' text in the buffer.")
            ser.write(rg_enter_key.encode())  
            ser.flush()
            time.sleep(0.5)            
            
            buffer = sercon.read_serialbuffer(buffer)
            
            if "root@Docsis-Gateway:~#" in buffer.decode():
                blogin = True
                buffer = bytes()
                
            # buffer = bytes()
            # while ser.in_waiting > 0:            
            #     buffer += ser.read(ser.in_waiting)            
            #     if ser.in_waiting == 0:
                    
            #         print(buffer.decode())
            #         #print(type(buffer.decode()))
            #         break
        # (3-2) 이미 RG console login이 된 경우, CM console을 open 하도록 
        elif blogin == True:
            print("RG console is already login.")
            blogin = False
            
            for j in range(0, 2):
                time.sleep(0.5)       
                ser.write(rg_enter_key.encode())  
                ser.flush()
                time.sleep(0.5)
                print("Entering the snmp cmd to enable CM console port.")
                ser.write(cm_console_open_cmd_str.encode())
                ser.flush()
                time.sleep(0.5)            

            buffer = sercon.read_serialbuffer(buffer)
            buffer = bytes()
        else:
            print("A Current buffer should be blank if RG console login process and snmp cmd set process have finished well.\n ")
            print("The current buffer is \n" + str(buffer.decode()))
            break
    
    # RG console 볼 일 다 봤으면 RG console logout 한다.
    time.sleep(0.5)       
    ser.write(rg_enter_key.encode())  
    ser.flush()
    time.sleep(0.5)
    ser.write(rg_logout_cmd_str.encode())
    ser.flush()
    time.sleep(0.5)
    
    buffer = sercon.read_serialbuffer(buffer)
    
    for i in range(0, 10):
        if "logout" in buffer.decode():
            print("RG console logout has done successfully.")
            buffer = bytes()
            break 
          
    # 열린 serial port로 필요한 작업을 완료 하고 난 뒤에는 닫는다.
    try:
        sercon.close_serial(com_port_info_rg)
    except Exception as e:
        print(f'Exception has occurred with this reason during close serial: {e}')    
    
    # pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass