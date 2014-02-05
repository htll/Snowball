#!/usr/bin/python3.3
# Snowball 2.0.1a
# Created by arch-angel
# Let Them Find Us / LTFU / lethemfind.us

'''
TODO: allow snowball to be run from the command line
e.g. python3 snowball.py --cpu > log.txt writes only cpu info to log file
Running python3 snowball.py without options should produce usage info and fail
to run.

Possible options:
--all (overrides all other options and provides full output)
--gen
--py
--env
--cpu
--net
--mem
--proc
--disk
'''

__version__ = "2.0.1a"

import psutil

import datetime
import platform
from collections import OrderedDict
import time


class InvalidMemType(Exception):
    '''Raised when memtype is not "swap" or "virtual".'''
    
    def __init__(self, mem):
        self.mem = mem
    
    def __str__(self):
        return repr(self.mem)


def print_start():
    '''Prints basic info about Snowball.'''
    
    print("Snowball " + __version__ + " by arch-angel")
    print("Generated " + datetime.datetime.now().strftime("%c"))


def get_env_info():
    '''Gets general information about the computer.'''
    
    infodict = OrderedDict()
    
    infodict["Name"] = platform.node()
    infodict["System"] = platform.system()
    infodict["System alias"] = " ".join(platform.system_alias(
            platform.system(), platform.release(), platform.version()))
    infodict["Platform"] = platform.platform()
    
    if infodict["System"] == "Linux": # System-specific information
        infodict["Distribution"] = " ".join(platform.dist())
    elif infodict["System"] == "Windows":
        infodict["OS"] = " ".join(platform.win32_ver())
    elif infodict["System"] == "MacOS":
        verinfo = platform.mac_ver()[1]
        macver = " ".join(platform.mac_ver())
        macver[1] = verinfo
        infodict["OS"] = " ".join(macver)
    
    infodict["Boot time"] = datetime.datetime.fromtimestamp(
            psutil.get_boot_time()).strftime("%c")
    infodict["Uptime"] = str(datetime.datetime.fromtimestamp(
            time.time() - psutil.get_boot_time()).strftime("%d:%H:%M:%S:%f"))
    
    for user in psutil.get_users():
        infodict["User '" + user.name + "' terminal"] = user.terminal
        infodict["User '" + user.name + "' host"] = user.host
        infodict["User '" + user.name + "' started"] = str(
                datetime.datetime.fromtimestamp(user.started).strftime("%c"))
    
    return infodict


def get_python_info():
    '''Gets information related to Python.'''
    
    infodict = OrderedDict()
    
    infodict["Implementation"] = platform.python_implementation()
    infodict["Version"] = platform.python_version()
    infodict["Build"] = " ".join(platform.python_build())
    infodict["Compiler"] = platform.python_compiler()
    
    if platform.system() == "Linux":
        infodict["libc version"] = " ".join(platform.libc_ver())
    
    return infodict


def get_cpu_info():
    '''Gets detailed CPU resource usage and statistics.'''
    
    infodict = OrderedDict()
   
    infodict["Processor"] = platform.processor()
    infodict["Architecture"] = platform.machine()
    infodict["Cores"] = str(psutil.NUM_CPUS)
    
    cores = int(infodict["Cores"])
    percent = psutil.cpu_times_percent(interval=0.1, percpu=True)
    
    if cores > 1:
        for core in range(0, cores):
            real_core = core + 1
            for time, _ in enumerate(percent[core - 1]):
                infodict["Core " + str(real_core) + " " + 
                    percent[core]._fields[time] + " usage"] = str(
                    percent[core][time]) + "%"
            
            infodict["Core " + str(real_core) + " total usage"] = str(
                    round(100.0 - getattr(percent[core], "idle"), 1)) + "%"
   
    timedict = OrderedDict()
    
    for name in percent[0]._fields:
        timedict[name] = 0.0
        
    for i, time in enumerate(percent[0]._fields):
        for core in range(0, cores):
            timedict[time] += percent[core][i]
   
    for time in timedict:
        timedict[time] = round(timedict[time] / cores, 1)
        infodict["Total " + time + " usage"] = str(timedict[time]) + "%"
   
    for core in range(0, cores):
        infodict["Total usage"] = 0.0
        infodict["Total usage"] += 100.0 - getattr(percent[core], "idle")
    
    infodict["Total usage"] = str(round(infodict["Total usage"]
            / cores, 1)) + "%"
    
    return infodict


def get_net_info():
    '''Gets information about network connections.'''
    
    infodict = OrderedDict()
    netstats = OrderedDict(sorted(psutil.net_io_counters(True).items()))
    
    for nic in netstats:
        for iostat, iotype in enumerate(vars(netstats[nic])):
            infodict[nic + " " + iotype] = str(netstats[nic][iostat])
    
    return infodict


def get_memory_info(memtype=""):
    '''Gets memory info. Memtype can be "swap" or "virtual".'''
    
    infodict = OrderedDict()

    if memtype == "swap" or memtype == "virtual":
        if memtype == "virtual":
            mem = psutil.virtual_memory()
        else:
            mem = psutil.swap_memory()
    else:
        raise InvalidMemType(memtype)
  	
    for item, val in enumerate(mem):
        infodict[mem._fields[item]] = str(val)
    
    for key in infodict:
        if key == "percent":
            infodict["percent used"] = infodict[key] + "%"
            del infodict[key]
        elif key != "percent used":
            infodict[key] += " bytes"
    
    return infodict


def get_disk_info():
    '''Gets disk information.'''
    
    infodict = OrderedDict()
    
    for partition in psutil.disk_partitions(True):
        if not partition.device:
            continue
        
        infodict[partition.device + " mount point"] = partition.mountpoint
        infodict[partition.device + " file system"] = partition.fstype
        infodict[partition.device + " options"] = partition.opts
        infodict[partition.device + " size"] = str(
                psutil.disk_usage(partition.mountpoint).total) + " bytes"
        infodict[partition.device + " free"] = str(
                psutil.disk_usage(partition.mountpoint).free) + " bytes"
        infodict[partition.device + " used"] = str(
                psutil.disk_usage(partition.mountpoint).used) + " bytes"
        infodict[partition.device + " percent used"] = str(
                psutil.disk_usage(partition.mountpoint).percent) + "%"
    
    return infodict


def print_info(info=dict()):
    '''Prints friendly output from get_*_info().'''
    
    for k, v in info.items():
        if not v and v != 0:
            v = "unknown"
        
        print(k + ": " + v)


# Print in order of volatility
print_start()
print("\nGeneral information:")
print_info(get_env_info())
print("\nPython information:")
print_info(get_python_info())
print("\nCPU information:")
print_info(get_cpu_info())
print("\nNetwork information:")
print_info(get_net_info())
print("\nProcess information:")
print(psutil.test())
print("\nMemory statistics:")
print("Virtual memory:")
print_info(get_memory_info("virtual"))
print("\nSwap/page memory:")
print_info(get_memory_info("swap"))
print("\nDisk information:")
print_info(get_disk_info())
print("\nWrite completed "
        + datetime.datetime.now().strftime("%c"))
