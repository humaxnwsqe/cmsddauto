from serialmanager import SerialManager
import time
# import serial.tools.list_ports as sp
import sys

from datahandle import DataHandler
from swversioncheckincm import SWVersionCheckingInCM # SWVersionCheckingInCM
from swversioncheckinpact import SWVersionCheckinginPACT
from confileimport import ConfigFileImport # ConfigFileImport
from confiledeploy import ConfigFileDeploy
from cmrebooting import CMRebooting
from config import Config
from cmmacinfo import CMMacInfoThroughSerial

global cm_ser_port

def main():
    
    # 변수들
    # global cm_ser_port
    rg_ser_port = ''
    cm_ser_port = ''
    cm_mac = ''
    
    upgd_conf_name = Config.UPGRADE_CONFIGURATION_FILE_NAME # v0.4.0
    
    
    #upgd_filename
    # cur_filename = "hgj310v4_v0.3.7.img"
    # upgd_filename = "hgj310v4_v0.4.0.img"
    
    cur_filename = Config.CURRENT_UPGRADEFILE_NAME
    upgd_filename = Config.UPGRADE_UPGRADEFILE_NAME
         
    #upgd_conf_name
    # cur_fw_ver = "Revision:  0.3.7"
    # target_fw_ver = "Revision:  0.4.0"
    #cur_fw_ver
    
    buffer = bytes()
    # The fisrt instance of SerialManager is only for finding serial ports' information.
    serial_info = SerialManager()
    
    if Config.MODEL_NAME_HGJ310V4:
        serial_info.get_rg_ssh_connection()
    else:
        rg_ser_port = serial_info.get_rg_serial_port_info()

    cm_ser_port = serial_info.get_cm_serial_port_info()
    del serial_info
    
    # If a CM console port information has found well, the CM console port information will be used to get CM MAC information through CMMacInfoThroughputSerial Class
    cm_mac_info_class = CMMacInfoThroughSerial(cm_ser_port)
    cm_mac = cm_mac_info_class.get_CM_Mac_Info()  
    del cm_mac_info_class 
    
    # The second instance of SerialManager is for executing automated SDD based on the found serial ports information.
    serial_connection = SerialManager(cm_ser_port)
    
       
    ####################################
    # Automated Secured SW Download(SSD)
    ####################################
    
    # Pre-condition #
    # This part is to open CM console serial.
    try:
        opened_serial = serial_connection.open_serial() # opened_serial
        opened_serial.reset_input_buffer()
        opened_serial.reset_output_buffer()
    except Exception as e:
        print(f'Exception has occurred with this reason: {e}')
    
    # Step 1. Version checking through CM console using the cmd 'version'    
    
    swver_check_in_cm = SWVersionCheckingInCM() # sw_version_checking
    current_swver = ""
    current_swver = swver_check_in_cm.get_swver_frm_cm(opened_serial, serial_connection) # current_sw_ver
    del swver_check_in_cm
    
    
    # Step 2. Getting SW upgrade file name from PACT
    
    sw_cur_filename = SWVersionCheckinginPACT(cm_mac, cur_filename)
    
    current_filename_in_conf = ""
    current_filename_in_conf = sw_cur_filename.get_filename_frm_conf()
    current_swver_in_conf = ""
    data_handler = DataHandler()
    current_swver_in_conf = data_handler.get_swver_frm_filename(current_filename_in_conf)
    
    
    # Step 3. Getting the target SW verion to be upgraded from user input data (type: str)
    
    target_swver = ""
    target_swver = data_handler.get_swver_frm_filename(upgd_filename)
    
    
    # Step 4. Check the sw version info from the console, PACT and user input data
    print(f"Current sw version in the DUT is '{current_swver}'.")
    print(f"Current sw verson in the configuration file is '{current_swver_in_conf}'.")
    print(f"The target SW vesrion te be upgraded is '{target_swver}'.")
    
    # Step 5. To check if the current DUT's sw version is different with the user input data
    bconf_import = False # To check the result of the configuration file import
    bconf_deploy = False # To check the result of the imported configuration file deployment
    # bdut_Reboot
    bdut_reboot = False # To check that the rebooting of DUT has done successfully
    
    # ? #
    # 사실 CM console 상에서 확인하는 SW 버전 정보와 PACT에 있는 config 
    # 파일 내 상 upgrade file name에 있는 버전 정보를 읽는 것은 둘 다 
    # SW 버전 정보를 확인하기 위함이다. CM console 상에서 얻은 
    # 버전 정보만 가지고 비교 하는 게 맞지 않나 싶다.
    
    if current_swver != target_swver or current_swver_in_conf != target_swver:
        
        
        # Step 5-1. The configuration file including the target sw file name will be imported to the tftpserver through PACT
        confile_import = ConfigFileImport(upgd_conf_name) #confile_import
        bconf_import = confile_import.import_target_confile()
        
        # Step 5-2. If the configuration file has imported successfully, this config file should be deployed.
        if bconf_import == True:
            bconf_import = False
            print("imported config file should be deployed.")
            confile_deploy = ConfigFileDeploy()
            bconf_deploy = confile_deploy.deploy_confile()
            
            # current_filename_in_conf
            current_filename_in_conf = sw_cur_filename.get_filename_frm_conf()
            
            del sw_cur_filename
            
            # To compare between user input target SDD file name and the file name from the imported configuration file for SDD. If both are not the same, SDD automation will be stopped by force.
            # 결국 config file에 있는 sw file name이 제대로 업데이트 된 상태가 아닐 경우를 확인하기 위함 임.
            if upgd_filename == current_filename_in_conf :
                sys.exit(f"Current file name for SDD:'{cur_swfilename_inconf}' is not the same as the target file name: '{upgd_filename}'.\n SDD Automation will be stopped forcibly!")
               
            
        # Step 5-3. If the deployment of the config file has finishd successfully, the DUT should be rebooted to start SW file download. 
        if bconf_deploy == True:
            bconf_deploy = False
            print("The DUT will be rebooted!")
            cm_reset = CMRebooting()
            bdut_reboot = cm_reset.cm_do_reset(opened_serial, serial_connection)
            if bdut_reboot == True:
                bdut_reboot = False
                print("F/W download will be started!!!")
         
        pass
    
    # Step 6. If the DUT has rebooted to download the new firmware, I want to know the progress of the download state like below. And the checking of state will be doing using while loop
    # Step 6-1. 'CM is OPERATIONAL'
    # Step 6-2. 'Storing to device' and 'Loading from server'
    # Step 6-3. 'we have reached end of file'
    # Step 6-4. 'Tftp transfer complete'
    # Step 6-5. 'NV write success' >> This is one of the loop exit conditions.
    # The time from step 6-1 to 6-5 may be different because it depends on the network envrionment condition. 
    # But in this code, the time does not over more 00 minutes. So if that time is over 00 minutes, this is another loop exit condition.
    # The loop of 'reading output buffer' > 'checking the buffer' > 'initailizing the buffer' is important because step 6-x conditions can be check through the output buffer  
    
        
    buffer = serial_connection.read_serialbuffer(buffer)
        
    try:
        serial_connection.close_serial(cm_ser_port)
        del serial_connection
    except Exception as e:
        print(f'Exception has occurred with this reason during close serial: {e}') 
        
    pass

if __name__ == "__main__": 
       
    main()
    pass