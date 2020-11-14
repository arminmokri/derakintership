#!/usr/bin/python3

# imports
import sys
import argparse
import subprocess, shlex
import re
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

def is_standard_fqdn(hostname: str):

    ### wiki reference
    # https://en.m.wikipedia.org/wiki/Fully_qualified_domain_name

    if not 1 < len(hostname) < 253:
        return False

    # Remove trailing dot
    if hostname[-1] == '.':
        hostname = hostname[0:-1]

    #  Split hostname into list of DNS labels
    labels = hostname.split('.')

    #  Define pattern of DNS label
    #  Can begin and end with a number or letter only
    #  Can contain hyphens, a-z, A-Z, 0-9
    #  1 - 63 chars allowed
    fqdn = re.compile(r'^[a-z0-9]([a-z-0-9-]{0,61}[a-z0-9])?$', re.IGNORECASE)

    # Check that all labels match that pattern.
    return all(fqdn.match(label) for label in labels)

def standard_fqdn(host):
    if not is_standard_fqdn(host):
        msg = host + " is not valid Standard FQDN"
        raise argparse.ArgumentTypeError(msg)
    return host

def traceroute_wrapper(command):
    traceroute_parser = argparse.ArgumentParser(description='')
    traceroute_parser.add_argument('-4', action='store_true', dest='ip4')
    traceroute_parser.add_argument('-6', action='store_true', dest='ip6')
    traceroute_parser.add_argument('-d', '--debug', action='store_true', dest='d')
    traceroute_parser.add_argument('-F', '--dont-fragment', action='store_true', dest='F')
    traceroute_parser.add_argument('-f', '--first', dest='f')
    traceroute_parser.add_argument('-g', '--gateway', dest='g')
    traceroute_parser.add_argument('-I', '--icmp', action='store_true', dest='I')
    traceroute_parser.add_argument('-T', '--tcp', action='store_true', dest='T')
    traceroute_parser.add_argument('-i', '--interface', dest='i')
    traceroute_parser.add_argument('-m', '--max-hops', '-maxh', dest='m')
    traceroute_parser.add_argument('-N', '--sim-queries', dest='N')
    traceroute_parser.add_argument('-n', action='store_true', dest='n')
    traceroute_parser.add_argument('-p', '--port', dest='p')
    traceroute_parser.add_argument('-t', '--tos', dest='t')
    traceroute_parser.add_argument('-l', '--flowlabel', dest='l')
    traceroute_parser.add_argument('-w', '--wait', dest='w')
    traceroute_parser.add_argument('-q', '--queries', dest='q')
    traceroute_parser.add_argument('-r', action='store_true', dest='r')
    traceroute_parser.add_argument('-s', '--source', dest='s')
    traceroute_parser.add_argument('-z', '--sendwait', dest='z')
    traceroute_parser.add_argument('-e', '--extensions', action='store_true', dest='e')
    traceroute_parser.add_argument('-A', '--as-path-lookups', action='store_true', dest='A')
    traceroute_parser.add_argument('-M', '--module', dest='M')
    traceroute_parser.add_argument('-O', '--options', dest='O')
    traceroute_parser.add_argument('--sport', dest='sport')
    traceroute_parser.add_argument('--fwmark', dest='fwmark')
    traceroute_parser.add_argument('-U', '--udp', action='store_true', dest='U')
    traceroute_parser.add_argument('-UL', action='store_true', dest='UL')
    traceroute_parser.add_argument('-D', '--dccp', action='store_true', dest='D')
    traceroute_parser.add_argument('-P', '--protocol', dest='P')
    traceroute_parser.add_argument('--mtu', action='store_true', dest='mtu')
    traceroute_parser.add_argument('--back', action='store_true', dest='back')
    traceroute_parser.add_argument('-V', '--version', action='store_true', dest='V')
    ###
    traceroute_parser.add_argument('host', type=standard_fqdn)
    traceroute_parser.add_argument('packetlen', nargs='?')
    ###
    args = traceroute_parser.parse_args(command.split())
    ###
    string = ""
    if not args.host == None:
        string = string + " " + args.host
    if not args.packetlen == None:
        string = string + " " + args.packetlen
    for arg in vars(args):
        varg = getattr(args, arg)
        if not (arg == "host" or arg == "packetlen"):
            if type(varg) == bool:
                if varg == True:
                    string = string + " -" + arg
            else:
                if not varg == None:
                    string = string + " -" + arg + " " + varg
    string = string.replace("-ip4", "-4")
    string = string.replace("-ip6", "-6")
    return string

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
            full_command = action + " " + traceroute_wrapper(args)
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
