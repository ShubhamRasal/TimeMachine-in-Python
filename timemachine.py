import sys
import argparse
import os
import datetime
from shutil import copy2
import logging

#create and configure logger
logging.basicConfig(filename="logs.log", 
                    format='%(asctime)s %(message)s')
#create an object
logger=logging.getLogger()

#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.DEBUG) 

##################################################################################################
#
#   function name:  copyfiles(config_file_path,des_folder_path)
#   Work: copy those files which are modified to destination location 
#
###################################################################################


def copyfiles(config_file_path,des_folder_path):
    try:

        with open(config_file_path,'r') as config_file:
                file_list = config_file.readlines()
                # print(file_list)
                
                for listx in file_list:
                    #get filename
                    temp= listx.split(" ")
                    datetime_str = temp[1]+" "+temp[2]           
                    #convert timestamp from str to datetime object
                    datetime_object=datetime.datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S.%f')
                    basename=os.path.basename(temp[0]).split(".")
                    #make destination path such that it is unique every time so that we can store multiple copies of single file
                    des_file = os.path.join(des_folder_path,basename[0]+'_'+str(datetime_object.year)+'_'+str(datetime_object.month)+'_'+str(datetime_object.day)+'_'+str(datetime_object.hour)+'_'+str(datetime_object.minute)+'.'+basename[1])
                   
                    #as we are using year,month,day,hrs,min in our file location  
                    if (os.path.exists(des_file) == False) :
                        try:
                           
                            copy2(temp[0],des_file)
                            logger.info('INFO:%s file added to destination with name : %s',temp[0],des_file)
                        except Exception as e:
                            logger.error("Exception occured",exc_info=True)
                            #print("Unexpected Error:",sys.exc_info())
                            #exit(1)
    except FileNotFoundError :
        logger.error('ERROR:%s File not Found.',config_file_path)
    except Exception as e:
        logger.error("ERROR:Exception occured",exc_info=True)

###############################################################################################
#
#   function : update_config(config_file_path)
#   work:   if any of file is modified then change its timestamp in config file else write as it is
##################################################################################################

def update_config(config_file_path):
    try:
        with open(config_file_path,'r') as config_file:
                file_list = config_file.readlines()
                # print(file_list)
        with open(config_file_path,'w') as config_file:

            for listx in file_list:
                #get filename and timestamp in datetime format
                temp= listx.split(" ")
                datetime_str = temp[1]+" "+temp[2]  
                #get old timestamp         
                old_timestamp=datetime.datetime.strptime(datetime_str,'%Y-%m-%d %H:%M:%S.%f')
                        
                #get current timestamp
                timestamp=os.path.getmtime(temp[0])
                #print("Timestamp:",timestamp)
                curr_timestamp= datetime.datetime.fromtimestamp(timestamp)
                #compare two timestamp to check it is modified or not 
                if old_timestamp != curr_timestamp:
                    config_file.write(temp[0] +" "+ str(datetime.datetime.fromtimestamp(timestamp))+" "+"\n" )
                else:
                    config_file.write(listx)

    except FileNotFoundError as e:
        logger.error('ERROR:File not Found.',exc_info=True)
    except Exception as e:
        logger.error("ERROR:Exception occured",exc_info=True)

                 



if __name__ == "__main__":
    config_file_path =os.path.join(os.getcwd(),'config.dat')    #default path configuration file
    des_folder_path =os.getcwd()                                #default path for destination

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="Add configuration path")
    parser.add_argument("--des", help="Add Destination of copies path")
    parser.add_argument("--add", help="Add Filename to config file")
    parser.add_argument("--remove", help="Remove given filename from config file")
    parser.add_argument("--list", help="Shows all the filenames in config file",action="store_true")
    args = parser.parse_args()
    
    # python timemachine.py --config configurationfile_path
    if args.config:
        #print("Inside config")
        try:
            if os.path.exists(args.config):
                config_file_path = args.config
            else:
                logger.error("ERROR:Wrong Configuration File path.")
        except Exception as e:
            logger.error("ERROR:Unexpected Exception Ouccured.",exc_info=True)
    #python timemachine.py --des Destinationfile_path
    if args.des:
        try:
            if os.path.exists(args.config):
                des_folder_path = args.des
            else:
                logger.error("ERROR:Wrong Destination Folder/directory  path.")
        except TypeError as e:
            logger.error("ERROR:TypeError: stat: path should be string, bytes, os.PathLike or integer, not NoneType")
            print("ERROR:TypeError: stat: path should be string, bytes, os.PathLike or integer, not NoneType")    
    # --add filepath           add filepath to congig file
    if args.add:
        try:
            config_file =open(config_file_path,'a')
            timestamp=os.path.getmtime(args.add)
            config_file.write(args.add +" "+ str(datetime.datetime.fromtimestamp(timestamp))+" "+"\n" )
        except FileNotFoundError as e:
            logger.error('ERROR:File not Found.',exc_info=True)
    
    # --remove filepath         remove filepath from config file
    if args.remove: 
        try:
            with open(config_file_path,'r') as config_file:
                file_list= config_file.readlines()
            with open(config_file_path,'w') as config_file:
                for line in file_list:
                    if args.remove not in line.strip("\n"):
                        config_file.write(line)
        except FileNotFoundError:
            logger.error('ERROR:File not Found.',exc_info=True) 
        except Exception as e:
            logger.error('ERROR:Unexpected Exception Ouccured',exc_info=True)          
    
    #--list              display filenames from config file
    if args.list:
        try:
            with open(config_file_path,'r') as config_file:
                file_list = config_file.readlines()
                for listx in file_list:
                    print(listx)
        except FileNotFoundError:
            logger.error('ERROR:File not Found.',exc_info=True) 
        except Exception as e:
            logger.error('ERROR:Unexpected Exception Ouccured',exc_info=True)

    update_config(config_file_path)
    copyfiles(config_file_path,des_folder_path)
    



   