#!/usr/bin/env python3

import sys
import re
import os
import psutil
from colorama import Fore, Style

PKG_NAME = "pinfo"
PKG_VERSION = "0.1"

proc_stat = {
    "D": "D: Uninterruptible sleep",
    "I": "I: Idle kernel thread",
    "R": "R: Running / Runnable",
    "S": "S: Interruptible sleep",
    "T": "T: Stopped by job control signal",
    "t": "t: Stopped by debugger",
    "W": "W: Paging",
    "X": "X: Dead",
    "Z": "Z: Zombie"
}

def get_comm(pid):
    f = open("/proc/{}/comm".format(pid))
    return f.read().rstrip()

def get_cmd(pid):
    f = open("/proc/{}/cmdline".format(pid))
    output = f.read().rstrip()
    if len(output) < 1:
        return "none"
    else:
        return output

def get_stat(pid):
    stat = []
    f = open("/proc/{}/stat".format(pid))
    output = f.read().split()

    name = ""
    name_flag = False
    for entry in output:
        if name_flag:
            if ")" in entry:
                name_flag = False
                name += " "
                name += entry
                stat.append(name)
                continue
            name += " "
            name += entry
            continue
        if "(" in entry:
            if ")" in entry:
                stat.append(entry)
                continue
            name_flag = True
            name += entry
            continue
        stat.append(entry)

    return stat

def get_env():
    f = open("/proc/{}/environ".format(pid))
    output = f.read().replace("\0", "\n").rstrip()
    if len(output) < 1:
        return "No output"
    else:
        return output

def get_loadavg():
    f = open("/proc/loadavg")
    output = f.read().split()[0:3]
    return " ".join(output)

def get_cpu_model():
    f = open("/proc/cpuinfo")
    for line in f:
        if "model name" in line:
            return line.split(":")[1].strip()

def get_utpime():
    f = open("/proc/uptime")
    output = f.read().split(" ")[0]
    days = float(output) / 60 / 60 / 24
    hours = float(output) / 60 / 60 % 24
    minutes = float(output) / 60 % 60
    return "{} Day(s), {} Hour(s), {} Minute(s)".format(int(days), int(hours), int(minutes))

def get_kernel():
    f = open("/proc/version")
    output = f.read().split(" ")[2]
    return output

def get_cpu_freq():
    return int(psutil.cpu_freq().max)

def get_cpu_count():
    return psutil.cpu_count()

def get_total_ram():
    return int(psutil.virtual_memory().total / 1048576)

def get_swap_used():
    return int(psutil.swap_memory().percent)

def get_root_usage():
    return int(psutil.disk_usage('/').percent)

def is_root():
    return os.getuid() == 0

def die(msg):
    print("[ERROR] {}".format(msg))
    sys.exit(1)

def usage():
    print("USAGE: pinfo PID")
    print("   PID    PID number of process to inspect")
    sys.exit(0)

def check_pid(pid):
    try:
        pid = int(pid)
    except:
        die("Not a PID number, exiting!")

    if not psutil.pid_exists(pid):
        die("ERORR: PID does not exist, exiting!")

if __name__ == "__main__":
    if not is_root():
        die("You need to run this script with root rights")

    if len(sys.argv) != 2:
        usage()

    pid = sys.argv[1]

    check_pid(pid)

    print("{}General System Info:{}".format(Style.BRIGHT + Fore.GREEN, Style.RESET_ALL + Fore.RESET))
    print("{:25s} {:25s}".format("CPU Model:", get_cpu_model()))
    print("{:25s} {:25s}".format("CPU Core Count:", str(get_cpu_count())))
    print("{:25s} {:25s}".format("Max CPU Frequency (Mhz):", str(get_cpu_freq())))
    print("{:25s} {:25s}".format("Loadavg:", get_loadavg()))
    print("{:25s} {:25s}".format("Total Memory (MB):", str(get_total_ram())))
    print("{:25s} {:25s}".format("Swap used (%):", str(get_swap_used())))
    print("{:25s} {:25s}".format("Utpime:", get_utpime()))
    print("{:25s} {:25s}".format("Kernel:", get_kernel()))
    print("{:25s} {:25s}".format("/ Usage (%):", str(get_root_usage())))
    
    print("\n{}Info Output for PID {}{}".format(Style.BRIGHT + Fore.GREEN, str(pid), Style.RESET_ALL + Fore.RESET))
    print("{:25s} {:25s}".format("Name:", get_comm(pid)))
    print("{:25s} {:25s}".format("cmdline:", get_cmd(pid)))
    stat_list = get_stat(pid)
    print("{:25s} {:25s}".format("State:", proc_stat[stat_list[2]]))
    print("{:25s} {:25s}".format("PPID:", stat_list[3]))
    print("{:25s} {:25s}".format("Process Group ID:", stat_list[4]))
    print("{:25s} {:25s}".format("Session ID:", stat_list[5]))
    print("{:25s} {:25s}".format("Nice value:", stat_list[18]))
    print("{:25s} {:25s}".format("Threads:", stat_list[19]))
    print("{:25s} {:25s}".format("VSS:", stat_list[22]))
    print("{:25s} {:25s}".format("RSS:", stat_list[23]))
    
    print("\n{}Environment Listing for PID {}{}".format(Style.BRIGHT + Fore.RED, str(pid), Style.RESET_ALL + Fore.RESET))
    print(get_env())
