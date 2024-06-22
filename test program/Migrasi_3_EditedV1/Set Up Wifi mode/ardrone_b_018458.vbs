Set cloner = CreateObject("WScript.Shell")
cloner.run "cmd"
WScript.Sleep 500

cloner.SendKeys"telnet 192.168.1.1"
cloner.SendKeys("{Enter}")
WScript.Sleep 500

cloner.SendKeys"killall udhcpd; iwconfig ath0 mode managed essid ardrone_server; ifconfig ath0 192.168.1.12 netmask 255.255.255.0 up;route add default gw 192.168.0.100"
cloner.SendKeys("{Enter}")
WScript.Sleep 500