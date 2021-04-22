from netmiko import ConnectHandler
#from validation_commands_infra import show_command_list
import sys

#show_command_list = open("validation_commands.txt").readlines()
#host_list=["10.205.142.80"]
def tnt_connect(host):
    tnt_session = ConnectHandler(
      device_type = "cisco_xr",
      host=host,
      username= "pldtadmin",
      password= "3nter_Me-1n2admin",
    )
    return tnt_session

def tnt_disconnect(tnt_session):
    tnt_session.disconnect()

def show_command(tnt_session,sh_command):
        command_out = tnt_session.send_command(sh_command,expect_string=r'#',delay_factor=5)
        return command_out

def save_to_file(command_out,host,command,activity):
    with open('/home/users/jraluta/tnt_script/UPGRADE/Data/' + host + '_' + activity + '.log', 'a') as parse_results:
              parse_results.write(command + '\n')
              parse_results.write("="*25 + '\n')
              parse_results.write(command_out + '\n')

def main():
    try:
       sys.argv[1]
       sys.argv[2]
    except:
       print('Specify if precheck,postcheck,test_case,test_case_pcc,show_run or remote_check and provide the host management IP')
       sys.exit(1)

    activity = sys.argv[1]
    myhost = sys.argv[2]
    host_list = [myhost]
    if "precheck" in activity or "postcheck" in activity:
        show_command_list = open("validation_commands.txt").readlines()
    if "test_case" in activity:
        show_command_list = open("validate_testcase.txt").readlines()
    if "remote_check" in activity:
        show_command_list = open("validate_remote.txt").readlines()
    if "show_run" in activity:
        show_command_list = open("show_run.txt").readlines()
    for host in host_list:
        print("Connecting to " + host + "...")
        tnt_sess = tnt_connect(host)
        if "precheck" in activity or "postcheck" in activity or "remote_check" in activity\
                or "show_run" in activity:
            for command in show_command_list:
                try:
                    command_out = show_command(tnt_sess,command)
                    save_to_file(command_out,host,command,activity)
                    print('Success ' + command + ' ' + myhost)
                except:
                    print('Failed ' + command + ' of ' + myhost)
            tnt_disconnect(tnt_sess)
            print("Disconnected " + host)
        if "test_case" in activity:
            for command in show_command_list:
                try:
                    command_out = show_command(tnt_sess,command)
                    #save_to_file(command_out,host,command,activity)
                    print(tnt_sess.find_prompt()+command)
                    print(command_out)
                except:
                    print('Failed ' + command + ' of ' + myhost)
            tnt_disconnect(tnt_sess)
            print("Disconnected " + myhost)
            pcc_host = ["10.205.138.19","10.205.138.96"]
            for host in pcc_host:
                tnt_sess_pcc = tnt_connect(host)
                pcc_command_list = open("pcc.txt").readlines()
                for command in pcc_command_list:
                    try:
                        command_out = show_command(tnt_sess_pcc, command)
                        # save_to_file(command_out,host,command,activity)
                        print(tnt_sess_pcc.find_prompt() + command)
                        print(command_out)
                    except:
                        print('Failed ' + command + ' of ' + host)
                tnt_disconnect(tnt_sess_pcc)
                print("Disconnected " + host)
    print("Done!")
if __name__ == '__main__':
    main()
