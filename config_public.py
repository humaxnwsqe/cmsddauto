# If you want to use this project, please change this file name from 'config_pubic.py' to 'config.py'.
# And some values in Class config should be written before using this file. 
# These values are related to the DUT's security. If you do not know these values, please contact to the right person who may know it in your team.





class Config:
    
    UPGRADE_CONFIGURATION_FILE_NAME = "*.cfg"
    CONFIGURATION_FILE_LOCAL_PATH = "localpath\\*.cfg"
    
    # APSOLUTE_PATH_OF_CONFIGURATION_FILE = ""
    CURRENT_UPGRADEFILE_NAME = "hgXXX_v1.1.img"
    UPGRADE_UPGRADEFILE_NAME = "hgXXX_v1.2.img"
    # PACT_URL_BASE = ""
    PACT_URL_BASE = ""
    PACT_URL_FOR_LISTDEVICES = PACT_URL_BASE + "/config/dhcp/deviceConfig.do?method=fetchLst"
    PACT_URL_FOR_CONFIGURATION_FILE_IMPORT = PACT_URL_BASE + "/tlvedit.do?method=fetchUpload"
    
    PACT_URL_FOR_CONFIGURATION_FILE_DEPLOY = PACT_URL_BASE + "/deploy.do?method=fetch&boatype=DHCP"
    PACT_CONFIGURATION_FILE_IMPORT_SUCCESS_MSG = "Uploaded successfully"
    PACT_CONFIGURATION_FILE_DEPLOY_SUCCESS_MSG = "DHCP deployment successful"
    
    KEY_ENTER = '\r'
    # Only one MODEL NAME constant should be chosen as True
    MODEL_NAME_HGJ310 = False # Common
    MODEL_NAME_HGJ310BR = False
    MODEL_NAME_HGJ310V4 = True
    
    if MODEL_NAME_HGJ310V4 == True:
        APSOLUTE_PATH_OF_MOBAXTERMEXE = "D:\MobaXterm_Portable_v22.0\MobaXterm_Personal_22.0.exe"
        MOBAXTERM_OPT_EXITWHENDONE = "-exitwhendone"
        MOBAXTERM_OPT_HIDETERM = "-hideterm"
        MOBAXTERM_OPT_BOOKMARK = "-bookmark"
        MOBAXTERM_OPT_SESSION = "rgconenable" # This is a mobaxterm's user define session. This seesion should be prepared seperately in the mobaxterm app to open hgj310v4 rg ssh console. If you want to know about the user defined mobaxterm session, please contact to the right IOP engineer.
        HGJ310_DEFAULT_GATEWAY_IP_ADD = "192.168.40.1"
        HGJ310_RG_SSH_LOGIN_ID = ""
        HGJ310_RG_SSH_LOGIN_PW = ""
        HGJ310_RG_SSH_PORT = 80
    
    SNMP_CMD_CM_CONSOLE_OPEN = "snmpset -v2c -c private xxx.xxx.xxx.xxx 1.3.6.1.4.1.4413.2.2.2.1.9.1.2.1.0 i 2"  
    
    # cm_cmd_movetoconsole = "cd Con"
    # cm_cmd_movetoconsole_str = cm_cmd_movetoconsole + cm_enter_key
    # cm_cmd_showip = "show ip"
    # cm_cmd_showip_str = cm_cmd_showip + cm_enter_key
    # cm_cmd_movetoroot = "cd /"
    # cm_cmd_movetoroot_str = cm_cmd_movetoroot + cm_enter_key
    
    CM_CMD_MOVETOCONSOLE = "cd Con"
    CM_CMD_MOVETOCONSOLE_STR = CM_CMD_MOVETOCONSOLE + KEY_ENTER
    CM_CMD_SHOWIP = "show ip"
    CM_CMD_SHOWIP_STR = CM_CMD_SHOWIP + KEY_ENTER
    CM_CMD_MOVETOROOT = "cd /"
    CM_CMD_MOVETOROOT_STR = CM_CMD_MOVETOROOT + KEY_ENTER
    CM_PATH_CM = "CM>"
    CM_PATH_CM_CONSOLE = "CM/CM_Console>"
    CM_CMD_RESET = "reset"
    CM_RESET_DONE_MSG = "Rebooting now so we don't trip all over ourselves"
    CM_FW_VER_EXPRESSION = "version"
    CM_FW_REVISION_EXPRESSION = "Revision:"
    
    RG_LOGIN_STATE_1ST = "Docsis-Gateway login"
    RG_LOGIN_STATE_2ND = "root@Docsis-Gateway:~#"
    
    
    
          
 
    pass