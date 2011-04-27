#!/usr/bin/env python

import subprocess
import sys
import getopt
from os.path import abspath, dirname, join

DEBUG_MODE = False

def _help():
    print """
NAME
    printRemotely.py: Copy the given file to the specified print server
    using scp. Then ssh into printserver and run lpr.

Warning: May overwrite existing files of the same name.

SYNOPSIS
    printRemotely.py [OPTIONS] [user@]printserver file

OPTIONS:
    -h / --help               Display this help
    -i SSH_PRIVATE_KEY        Use this private key for scp and ssh connections
    -P PRINTERNAME            Use the specified printer
    -d                        Delete the file on the server after printing

INSPIRATION:
    Karan Malik

AUTHOR:
    Seshadri Mahalingam (seshadri@berkeley.edu)
    
"""
    sys.exit()

try:
    opts, args = getopt.getopt(sys.argv[1:], 
                               "hi:P:Z:d",
                               ["help", "duplex"])
    sshOptions = ""
    lprOptions = ""
    deleteFile = False
    
    for o,a in opts:
        if o in ('-h', '--help'):
            _help()
        elif o == "-i":
            sshOptions += o + " " + a
        elif o in ("-P", "-Z"):
            lprOptions += o + " " + a
        elif o == "--duplex":
            if lprOptions.find("-Z duplex") == -1:
                lprOptions += " " + "-Z duplex"
        elif o == "-d":
            deleteFile = True
        elif o == "--debug":
            DEBUG_MODE = True

    if len(args) != 2:
        print "Invalid arguments. Try --help."
        sys.exit(2)

    filename = args[1].split('/')[-1]

    scpCommand = "scp" + (" " + sshOptions if sshOptions != "" else "") + \
        ' "' + args[1] + '" ' + args[0] + ":"
    lprCommand = ("lpr" if not DEBUG_MODE else "ls") + \
        (" " + lprOptions if lprOptions != "" else "") + \
        ' "' + filename + '"'
    sshCommand = 'ssh' + (" " + sshOptions if sshOptions != "" else "") + \
        ' ' +  args[0] + ' "' + lprCommand + \
        ("; rm " + filename if deleteFile else "")  + '"'

    print scpCommand
    subprocess.call(scpCommand, shell=True)

    print sshCommand
    subprocess.call(sshCommand, shell=True)

except getopt.GetoptError, err:
    # print help information and exit:
    print str(err) # will print something like "option -a not recognized"
    print "Try --help for valid options"
    sys.exit(2)
