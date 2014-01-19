# Snowball 2.0a
# Created by arch-angel
# Let Them Find Us / LTFU / lethemfind.us

'''
Dependency information:
Python 3.3
psutil 1.2.1
'''

# First, check to see if we have psutil
import sys
try:
    import psutil
except ImportError:
    # Exit if we don't have psutil
    print("psutil not installed. Exiting.")
    sys.exit(1)

# Import modules in the order they appear
import datetime, platform
from collections import OrderedDict

def print_start():
    '''Prints basic info about Snowball.'''
    ver = "2.0a"
    print("Snowball " + ver + " by arch-angel")
    print("Generated " + str(datetime.datetime.now()))

# Data collection functions
def get_env_info():
    '''Gets general information about the computer.'''
    infodict = OrderedDict()
    infodict["Name"] = platform.node()
    infodict["System"] = platform.system()
    infodict["System alias"] = " ".join(platform.system_alias(platform.system(), platform.release(), platform.version()))
    infodict["Platform"] = platform.platform(True, False)
    
    if infodict["System"] == "Linux":
        infodict["Distribution"] = " ".join(platform.dist())
    elif infodict["System"] == "Windows":
        infodict["OS"] = " ".join(platform.win32_ver())
    elif infodict["System"] == "MacOS":
        verinfo = platform.mac_ver()[1]
        macver = " ".join(platform.mac_ver())
        macver[1] = verinfo
        infodict["OS"] = " ".join(macver)
        
    # TODO: Add users
    
    return infodict

def get_python_info():
    '''Gets information related to Python.'''
    infodict = OrderedDict()
    infodict["Implementation"] = platform.python_implementation()
    infodict["Version"] = platform.python_version()
    infodict["Build"] = " ".join(platform.python_build())
    infodict["Compiler"] = platform.python_compiler()
    
    return infodict

def get_cpu_info():
    '''Gets detailed CPU resource usage and statistics.'''
    infodict = OrderedDict()
    
    # Add constant (fixed) information
    infodict["Processor"] = platform.processor()
    infodict["Architecture"] = platform.machine()
    infodict["Cores"] = str(psutil.NUM_CPUS)
    
    cores = int(infodict["Cores"]) # In variable for faster referencing
    percent = psutil.cpu_times_percent(1, True) # In variable for constant data
    if cores > 1:
        for core in range(0, cores):
            real_core = core + 1 # In variable for faster referencing
            for time, _ in enumerate(percent[core - 1]):
                infodict["Core " + str(real_core) + " " + \
                percent[core]._fields[time] + \
                " usage"] = str(percent[core][time]) + "%"
            # Total core usage
            infodict["Core " + str(real_core) + " total usage"] \
            = str(round(100.0 - getattr(percent[core], "idle"), 1)) + "%"
    
    # For every value in 'percent', get those values in each core,
    # add them together, divide by the number of cores, then store it
    
    # 1. Set up the ordered dictionary with the same fields as 'percent'
    timedict = OrderedDict()
    for name in percent[0]._fields:
        timedict[name] = 0.0
    
    # 2. Add the values of each field from each core together
    for i, time in enumerate(percent[0]._fields):
        for core in range(0, cores):
            timedict[time] += percent[core][i]
    
    # 3. Divide each value by the number of cores
    for time in timedict:
        timedict[time] = round(timedict[time] / cores, 1)
        infodict["Total " + time + " usage"] = str(timedict[time]) + "%"
    
    # Total CPU usage
    for core in range(0, cores):
        infodict["Total usage"] = 0.0
        infodict["Total usage"] += 100.0 - getattr(percent[core], "idle")
    
    infodict["Total usage"] = str(round(infodict["Total usage"] \
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

def get_process_info(info):
    '''Gets detailed information about currently running processes.'''
    infodict = OrderedDict()
    
    # TODO: Clean this up
    
    '''
    
    # This must be stored in a variable to prevent "No Such Process" exceptions
    proclist = psutil.get_process_list()
    
    for process in proclist:
        
        getprocess = psutil.Process(process.pid)
        
        infodict[str(process.pid)] = getprocess.name + ", " + \
        getprocess.username + ", " + \
        getprocess.status + ", " + \
        str(getprocess.ppid) + ", " + \
        str(getprocess.get_children()) + ", " + \
        str(getprocess.cmdline) + ", " + \
        str(getprocess.get_threads()) + ", " + \
        str(getprocess.get_cpu_affinity()) + ", " + \
        str(getprocess.get_num_ctx_switches()) + ", "
        
        '\''
        if platform.system() == "Linux":
            infodict[str(process.pid)] += str(getprocess.get_num_fds())
        else:
            infodict[str(process.pid)] += "unavailable"
            
        infodict[str(process.pid)] += ", "
        
        if platform.system() == "Windows":
            infodict[str(process.pid)] += str(getprocess.get_num_handles())
        else:
            infodict[str(process.pid)] += "unavailable"
            
        #infodict[str(process.pid)] += ", " + \
        
        try:
            infodict[str(process.pid)] = str(getprocess.get_open_files()) + ", "
        except psutil._error.AccessDenied:
            infodict[str(process.pid)] = "denied, "
        
        try:
            infodict[str(process.pid)] = str(getprocess.get_connections()) + ", "
        except psutil._error.AccessDenied:
            infodict[str(process.pid)] = "denied, "
        
        '\''infodict[str(process.pid)] += ", " + "threads: <"
        for threadnum, thread in enumerate(getprocess.get_threads()):
            if threadnum :
                infodict[str(process.pid)] += ", "
            infodict[str(process.pid)] += str(threadnum)
        infodict[str(process.pid)] += ">"
        '''
    return infodict
    
    '\''

def get_memory_info(memtype):
    '''Gets memory info. Memtype = str, can be "swap" or "virtual"'''
    infodict = OrderedDict()
    
    if memtype == "swap" or "virtual":
        if memtype == "virtual":
            mem = psutil.virtual_memory()
        else:
            mem = psutil.swap_memory()
    else:
        print("Internal error: invalid memory type.")
        sys.exit(2)
  	
    for item, val in enumerate(mem):
        infodict[mem._fields[item]] = str(val)
    
    for key in infodict:
        if key == "percent":
            infodict["percent used"] = infodict[key] + "%"
            del infodict[key]
        elif key != "percent used":
            infodict[key] += " bytes"
    
    return infodict

# Data printing functions
def print_info(info):
    '''Prints friendly output from get_*_info(). info = dict or OrderedDict'''
    
    for key, value in info.items():
        # Change blank values to "unknown"
        if value == "" or None:
            value = "unknown"
        print(key + ": " + value)

# Print data here
# Note: print in order of volitility
print_start()
print("")
print("General information:")
print_info(get_env_info())
print("")
print("Python information:")
print_info(get_python_info())
print("")
print("CPU information:")
print_info(get_cpu_info())
print("")
print("Network information:")
print_info(get_net_info())

# TODO: Clean this up
'''
print("Process list:")
print("PID, name, owner, status, parent pid, children, invoked as, threads, affinity, ctx switches, handles, files open, connections open, memory, memory maps")
print_info(get_process_info())
'''
print("")
print("Memory statistics:")
print("Virtual memory:")
print_info(get_memory_info("virtual"))
print("")
print("Swap/page memory:")
print_info(get_memory_info("swap"))
