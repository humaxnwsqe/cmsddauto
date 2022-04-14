import serial
import serial.tools.list_ports as sp
import time
import math
from config import Config
import psutil
import subprocess
import paramiko

class SerialManager():
    
    # port = None
    
    # def __init__(self, port):
    #     self.port = port
    #     self.ser = serial.Serial()
    
    def __init__(self, port = None):
        
        if port == None:    
            self.ser = serial.Serial()
            return
        self.port = port
        self.ser = serial.Serial()
        
    
    def open_serial(self, port = None, baudrate=115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False):
        
        #ser = serial.Serial()    
        if port == None:
            self.ser.port = self.port
        else:
            self.ser.port = port
            
        self.ser.baudrate = baudrate
        self.ser.bytesize = bytesize
        self.ser.parity = parity
        self.ser.stopbits = stopbits
        # ser.timeout = timeout 
        # there are three option in timeout (1) None, (2) 0, (3) x (sec)
        # timeout = None: wait forever / until requested number of bytes are received
        # timeout = 0: non-blocking mode, return immediately in any case, returning zero or more, up to the requested number of bytes
        # timeout = x: set timeout to x seconds (float allowed) returns immediately when the requested number of bytes are available, otherwise wait until the timeout expires and return all bytes that were received until then.
        self.ser.timeout = 0
        self.ser.xonxoff = xonxoff
        self.ser.rtscts = rtscts
        self.ser.dsrdtr = dsrdtr
        
        # Before serial connection open
        if self.ser.is_open == True:
            raise Exception(f"The com_port {self.ser.port} is not available. Please choose the right com port.")
        
        # To open the target serial port
        self.ser.open()
        
        # After serial connection is success
        if self.ser.is_open == True:
            print(f"Current {self.ser.port} is available. We will use this port!")            
        else:
            raise Exception(f"Something wrong happend during serial connection with {self.ser.port}.")
            
        
        return self.ser
    
    def close_serial(self, port):
        print(f"The current open port '{port}' will be closed.")
        
        if self.ser.is_open == True:
            self.ser.cancel_write()
            self.ser.cancel_read()
            self.ser.close()
        
        return
    
    # This method is for reading buffer after console commands writting finished.
    # The exit condition of the loop in this method is that there will be no more data to read in the buffer. 
    #  read_serialbuffer > read_serialbuffer
    def read_serialbuffer(self, buffer):
        # time.sleep(2)
        # ser = serial
        # tmp_buf = bytes()
        tmp_buf = buffer
        
        print("read_serialbuffer method is start")
        
        # i = 0
        
        #time.sleep(1)
        while self.ser.in_waiting > 0:  
            # print(i)
            time.sleep(.1)   
            tmp_buf += self.ser.read(self.ser.in_waiting)
            time.sleep(.1)
            if self.ser.in_waiting == 0:
                
                # print("sermanager.py > read_serialbuffer")
                #print("Case: ser.in_waiting == 0 > " + tmp_buf.decode())
                print(tmp_buf.decode())
                break
            # i = i + 1
        
        return tmp_buf
    
    # This method is for reading buffer to check the printed buffer is the condition what we want or not. e.g  f/w download

    # It should be changed to check printed log continuously unitl the NVRAM writing end condition. 
    # And the return value is not fixed yet. Candidate types are boolean, list??
    # def read_serialbuffer_fwdn(self, buffer):
    def read_serialbuffer_fwdn(self, strlist):
        # time.sleep(2)
        # ser = serial
        # tmp_buf = bytes()
        # tmp_buf = buffer        
        
        # lines = tmp_buf.decode().splitlines()
        
        print("===============================================")
        print("read_serialbuffer_fwdn(f/w download) method start!")
        print("===============================================")
        
        self.ser.reset_output_buffer()
        
        tmp_len = len(strlist)
        
        # i = 0
        
        t_start = time.time()
        t_trunspent = 0
        
        b_cmon = False
        b_loadfrmserv = False
        b_store2dev = False
        b_tftpdnend = False
        b_tftpdnend2 = False
        b_nwwrtsuc = False
        
        file = open("./buffer.txt", mode="w")
        file.close()
        #time.sleep(1)
        # while (self.ser.in_waiting > 0) and (t_trunspent < 900):
        while True and (t_trunspent < 1500):  
            t_next = time.time()            
            t_trunspent = math.trunc(t_next - t_start)
            
            # print(i)
            
            if self.ser.readable():
                # time.sleep(.01)
                res = self.ser.readline()
                time.sleep(.01)
                cur_lineinbuffer = res.decode()[:len(res)-1]
                
                # print(cur_lineinbuffer)
                # file.write(cur_lineinbuffer)
                
                if strlist[0] in cur_lineinbuffer:
                    if b_cmon == False:
                        print(f"{strlist[0]} is in the buffer.")
                        with open("./buffer.txt", mode="a") as file:
                            file.write(cur_lineinbuffer)
                        b_cmon = True
                elif strlist[1] in cur_lineinbuffer:
                    if b_loadfrmserv == False:
                        print(f"{strlist[1]} is in the buffer.")
                        with open("./buffer.txt", mode="a") as file:
                            file.write(cur_lineinbuffer)
                        b_loadfrmserv = True
                elif strlist[2] in cur_lineinbuffer:
                    if b_store2dev == False:
                        print(f"{strlist[2]} is in the buffer.")
                        with open("./buffer.txt", mode="a") as file:
                            file.write(cur_lineinbuffer)
                        b_store2dev = True
                elif strlist[3] in cur_lineinbuffer:
                    if b_tftpdnend == False:
                        print(f"{strlist[3]} is in the buffer.")
                        with open("./buffer.txt", mode="a") as file:
                            file.write(cur_lineinbuffer)
                        b_tftpdnend = True
                elif strlist[4] in cur_lineinbuffer:
                    if b_tftpdnend2 == False:
                        print(f"{strlist[4]} is in the buffer.")
                        with open("./buffer.txt", mode="a") as file:
                            file.write(cur_lineinbuffer)
                        b_tftpdnend2 = True
                elif strlist[5] in cur_lineinbuffer:
                    if b_nwwrtsuc == False:
                        print(f"{strlist[5]} is in the buffer.")
                        with open("./buffer.txt", mode="a") as file:
                            file.write(cur_lineinbuffer)
                            file.write("\nf/w download and writing it to nvram have finished successfully!")
                            file.write(f"\nIt took {t_trunspent} seconds.")
                        b_nwwrtsuc = True
                        break
                
                # for i in range(0, tmp_len):
                #     if strlist[i] in cur_lineinbuffer:
                #         print(f"{strlist[i]} is in the buffer.")
                
            # time.sleep(.1)   
            # tmp_buf += self.ser.read(self.ser.in_waiting)
            # time.sleep(.1)
            
            # if t_trunspent % 100 == 0:
            #     print (f"{t_trunspent} seconds passed!")
            
            # # If 10 secs passes after this method has excuted 
            # if t_trunspent % 10 == 0:                
            #     pass
                # print("sermanager.py > read_serialbuffer")
                #print("Case: ser.in_waiting == 0 > " + tmp_buf.decode())
                # print(tmp_buf.decode())
                # break
            
            # i = i + 1
            # time.sleep(1)
        # file.close()
        
        # return tmp_buf
    
        
    def check_comport(self, targetport):
        
        port = self.port
        bport = False
        
        list = sp.comports()
        
        connected = []
        
        for i in list:
            connected.append(i.device)
        
        print("Connected COM ports: " + str(connected))
        
        if targetport in connected:
            bport = True
            
        return bport
    
    if Config.MODEL_NAME_HGJ310V4:
        def get_rg_ssh_connection(self):
            
            # To kill one or more mobaxterm processes before we try to run the mobaxterm's session.
            kill_execution_app("MobaXterm")    
            
            l_cmd = [Config.APSOLUTE_PATH_OF_MOBAXTERMEXE,
                    Config.MOBAXTERM_OPT_EXITWHENDONE,
                    Config.MOBAXTERM_OPT_HIDETERM,
                    Config.MOBAXTERM_OPT_BOOKMARK,
                    Config.MOBAXTERM_OPT_SESSION]
            
            outputs = subprocess.Popen(
                    l_cmd, 
                    stdout=subprocess.PIPE,                
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    shell=True) 
            
            time.sleep(1)   
            print(outputs)  
            
            # To kill the mobaxterm's session to enable hgj310v4's rg ssh console
            kill_execution_app("MobaXterm")       

            cli = paramiko.SSHClient()
            cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            
            server = Config.HGJ310_DEFAULT_GATEWAY_IP_ADD  
            user = Config.HGJ310_RG_SSH_LOGIN_ID  
            pwd = Config.HGJ310_RG_SSH_LOGIN_PW
            port = Config.HGJ310_RG_SSH_PORT # integer type
            
            time.sleep(1)
            cli.connect(server, port=port, username=user, password=pwd)
            # 2022.03.25 위 라인까지는 SSH 열었음.
            time.sleep(1)
            
            # 열린 SSH에서 Linux cli 동작 여부 확인 
            stdin, stdout, stderr = cli.exec_command("ls -al")
            lines = stdout.readlines()
            print(''.join(lines))
            lines = []
                        
            ########################
            # 그 다음에는 CM serial console 열도록 처리 해야 함 
            ########################
            
            stdin, stdout, stderr = cli.exec_command(Config.SNMP_CMD_CM_CONSOLE_OPEN)
            lines = stdout.readlines()
            print(''.join(lines))
            lines = []
            
            return ''
            
    
    def get_rg_serial_port_info(self):
        
        # port = self.port
        bport = False
        rg_serial_port = ''
        enter_key = Config.KEY_ENTER #"\r"
        buffer = bytes()
        
        list = sp.comports()
        
        connected = []
        
        if len(list) > 0:
            for i in list:
                connected.append(i.device)
        else:
            sys.exit("There is no available serail port in your environment.\
                \nPlease check the serial cables are connected with the DUT.")
        
        print("Connected COM ports: " + str(connected))
        
        for i in range(0, len(connected)):
            ser_port_info = str(connected[i])
            
            ser = self.open_serial(ser_port_info)
            
            ser.reset_input_buffer()
            ser.reset_output_buffer() 
                
            time.sleep(0.5)
            ser.write(enter_key.encode())  
            ser.flush()
            time.sleep(0.5)
            
            buffer = self.read_serialbuffer(buffer)
            print(buffer.decode())
            
            if Config.RG_LOGIN_STATE_1ST in buffer.decode() or \
                Config.RG_LOGIN_STATE_2ND in buffer.decode():
                rg_serial_port = ser_port_info
                print(f"We found the RG console port info.\
                    \nThe current RG console port is '{ser_port_info}' !.\
                    \nThis port information will be returned.")
                self.close_serial(ser_port_info)
                break
            else:
                print(f"'{ser_port_info}' is not the RG console.")
                self.close_serial(ser_port_info)
                        
            buffer = bytes()
        
        if rg_serial_port == '':
            sys.exit(f"One of {str(connected)} is disconnected from the DUT.\
                \nPlease check the serial cable's state.")
                    
        return rg_serial_port
    
    def get_cm_serial_port_info(self):
        
        # port = self.port
        bport = False
        cm_serial_port = ''
        enter_key = Config.KEY_ENTER # "\r"
        buffer = bytes()
        
        list = sp.comports()
        
        connected = []
        
        if len(list) > 0:
            for i in list:
                connected.append(i.device)
        else:
            sys.exit("There is no available serail port in your environment.\
                \nPlease check the serial cables are connected with the DUT.")
        
        print("Connected COM ports: " + str(connected))
        
        for i in range(0, len(connected)):
            ser_port_info = str(connected[i])
            
            ser = self.open_serial(ser_port_info)
            
            ser.reset_input_buffer()
            ser.reset_output_buffer() 
                
            time.sleep(0.5)
            ser.write(enter_key.encode())  
            ser.flush()
            time.sleep(0.5)
            
            buffer = self.read_serialbuffer(buffer)
            
            if "CM>" in buffer.decode() or \
                "CM" in buffer.decode():
                cm_serial_port = ser_port_info
                print(f"We found the CM console port info.\
                    \nThe current CM console port is '{ser_port_info}' !.\
                    \nThis port information will be returned.")
                self.close_serial(ser_port_info)
                break
            else:
                print(f"'{ser_port_info}' is not the CM console.")
                self.close_serial(ser_port_info)
                        
            buffer = bytes()
        
        if cm_serial_port == '':
            sys.exit(f"One of {str(connected)} is disconnected from the DUT.\
                \nPlease check the serial cable's state.")
                 
        return cm_serial_port
    
# A method to kill the target application before the execution of the application like MobaXterm.   
def kill_execution_app(appName):
    
    if(type(appName)==str):
        tmpAppName = appName 
    elif appName == '':
        print(f"Cls: SerialManager > Method: kill_execution_app's 1st param: {appName} is blank. \nPlease check the param you used in your code.")
        return
    else:
        print(f"Cls: SerialManager > Method: kill_execution_app's 1st param: {appName} is not a type of string . \nPlease check the param you used in your code.")
        return 
    
    for proc in psutil.process_iter():
        ps_name = proc.name()
        if tmpAppName in ps_name: # MobaXterm
            print(ps_name)
            print(int(proc.pid))
            parent = psutil.Process(int(proc.pid))
            for child in parent.children(recursive=True):
                child.kill()
            parent.kill()
    
    return
    