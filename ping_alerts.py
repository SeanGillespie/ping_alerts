'''
Simple program to play audio alerts if hosts can or cannot be reached with a ping.

Use Case: When you are replacing or configuring something on a network and want to be alerted
when something goes down or up.  This is much easier and hands/eyes off compared to opening 
a bunch of terminals and manually pinging each host and watching for a change. All you need to do
is run the program with the relevant hosts as arguments and place the computer within earshot to
know if something happens.

@authour: Sean Gillespie
'''
import subprocess
import argparse
import os
import sys
import logging
from gtts import gTTS

#continuously pings all hosts once, and plays audio specifying if a host is up
def alert_up(hosts):

    #creates an mp3 file that will say the name of the host and that it is up (if it does not exist)"
    #example, if one of the hosts is 10.10.10.10, a file will be created saying "10.10.10.10 is up"
    for host in hosts:
        if not os.path.exists('mp3\\' + host + '_up.mp3'):
            msg = host + ' is up'
            sound = gTTS(text=msg, lang='en', slow=False)
            sound.save('mp3\\' + host + '_up.mp3')

    #loops through the hosts and pings once. If up, plays matching mp3 file
    while True:
        for host in hosts:
            command = 'ping -n 1 '
            command += host
            command = command.split()
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            output = proc.stdout.read()
            output = output.decode()
            #if TTL is in the output, that means we pinged and got a response
            if "TTL" in output:
                logging.warn(output)
                command = 'start mp3\\' + host + '_up.mp3'
                os.system(command) 


#continuously pings all hosts once, and plays audio specifying if a host is down
def alert_down(hosts):

    #creates an mp3 file that will say the name of the host and that it is down (if it does not exist)"
    #example, if one of the hosts is 10.10.10.10, a file will be created saying "10.10.10.10 is down"
    for host in hosts:
        if not os.path.exists('mp3\\' + host + '_down.mp3'):
            msg = host + ' is down'
            sound = gTTS(text=msg, lang='en', slow=False)
            sound.save('mp3\\' + host + '_down.mp3')

    #loops through the hosts and pings once. If down, plays matching mp3 file
    while True:
        for host in hosts:
            command = 'ping -n 1 '
            command += host
            command = command.split()
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            output = proc.stdout.read()
            output = output.decode()
            #If there is no TTL in output, it is either down or not reachable 
            if "TTL" not in output:
                logging.warn(output)
                command = 'start mp3\\' + host + '_down.mp3'
                os.system(command) 

def main():

    #use logging so that we can see what specifically is happening on an instance of up or down, depending what we are doing
    logging.basicConfig(level=logging.WARN)

    my_parser = argparse.ArgumentParser(description='ping a list of IP addresses and play sound if down or play sound if up')
    my_parser.add_argument('-l', '--list', nargs='+', action='store', required=True, type=str, dest='hosts', default='', help='list of hostnames to ping and alert if DOWN')
    my_parser.add_argument('-u', '--up', action='store_true', dest='up_flag', default=False, help='alert if hosts are UP')
    args = my_parser.parse_args()

    #if there is no directory to put the mp3 files, we make one as not to clutter cwd
    if not os.path.exists('mp3'):
        os.mkdir('mp3')

    #if the -u argument is present, play mp3 alerts if a host is up instead of the default down
    if args.up_flag:
        alert_up(args.hosts)
    else:
        alert_down(args.hosts)

main()
