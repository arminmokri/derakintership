#!/usr/bin/python3

# imports
import sys
import argparse
import subprocess, shlex 
derak_parser = None
exit_code = 0

def execute_system_command(command):
    args = shlex.split(command)
    popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    std_out, std_err = popen.communicate()
    return (popen.returncode, std_out, std_err)

def usage():
    derak_parser.print_help()
    return
 
def print_execute_system_command(status, std_out, std_err):
    if status != 0:
        usage()
        print(std_err, file=sys.stderr)
    print(std_out)

def main():
    global derak_parser
    global exit_code
    try:
        # make derak parser
        derak_parser = argparse.ArgumentParser(description='This app is for derak cloud inc.')
        derak_parser.add_argument('action', choices=["dig", "traceroute", "whois", "curl"])

        # split comment from args
        action = sys.argv[1]
        args = ' '.join([str(args) for args in sys.argv[2:]])
        full_command = ' '.join([str(full_command) for full_command in sys.argv[1:]])

        # parse args
        derak_parser.parse_args(action.split())
    
        # decision
        if action == "dig":
            (status, std_out, std_err) = execute_system_command(full_command)
            print_execute_system_command(status, std_out, std_err)
            exit_code = status
        elif action == "traceroute":
            # need to change and valid args later
            (status, std_out, std_err) = execute_system_command(full_command)
            print_execute_system_command(status, std_out, std_err)
            exit_code = status
        elif action == "whois":
            (status, std_out, std_err) = execute_system_command(full_command)
            print_execute_system_command(status, std_out, std_err)
            exit_code = status
        elif action == "curl":
            (status, std_out, std_err) = execute_system_command(full_command)
            print_execute_system_command(status, std_out, std_err)
            exit_code = status
    except Exception as e:
        print(e)
        usage()
    finally:
        exit(exit_code)

if __name__ == "__main__":
    main()
