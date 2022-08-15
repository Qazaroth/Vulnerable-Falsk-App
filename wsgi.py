from run import app

import netifaces, winreg, os

def getConnectionNameFromGUID(ifaceGuids):
    ifaceNames = ["(Unknown)" for i in range(len(ifaceGuids))]
    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    reg_key  = winreg.OpenKey(reg, r"SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}")

    for i in range(len(ifaceGuids)):
        try:
            reg_subkey = winreg.OpenKey(reg_key, ifaceGuids[i] + r"\Connection")
            ifaceNames[i] = winreg.QueryValueEx(reg_subkey, "Name")[0]
        except FileNotFoundError:
            pass
    
    return ifaceNames

# ip = "192.168.108.129" # VMnet3
# ip = "192.168.145.128" # NAT

netInterfaces = netifaces.interfaces()

wifiIF = netInterfaces[-2]

vmnet3IF = netInterfaces[-4]

if os.name in ("nt", "dos"):
    connectionNames = getConnectionNameFromGUID(netInterfaces)
    wifi = connectionNames[-2]
    vmnet3 = connectionNames[-4]

if __name__ == "__main__":
    wifiIP = netifaces.ifaddresses(wifiIF)[netifaces.AF_INET][0].get("addr", "0.0.0.0")
    vmnetIP = netifaces.ifaddresses(vmnet3IF)[netifaces.AF_INET][0].get("addr", "0.0.0.0")
    print(wifiIP)
    print(vmnetIP)
    #app.run(port=8000)#ip, 8000)