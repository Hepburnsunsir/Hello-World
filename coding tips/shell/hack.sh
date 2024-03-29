#!/bin/sh

# get IP address of receiver's main interface for use in HTTP requests to self
# web server is not bound to localhost, so this IP has to be used
ip_address=$(/sbin/ifconfig | grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}" | grep -v 127.0.0.1 | awk '{print $2}' | cut -f2 -d:)

# POST helper function
sendRequest() {
    content=$1
    length=${#content}
    header="POST /cgi-bin/json_xfer HTTP/1.1\r\nHost: $ip_address\r\nContent-Type: application/json\r\nContent-Length: $length\r\nAuthorization: Basic bnVueWE6YnVzaW5lc3M=\r\n\r\n"
    echo -e "${header}" "${content}" | nc "$ip_address" 80
}

# JSON POST data to send "power on" serial command
jsonSerialPowerOn='{"params":{"TVCtrlType":"serial","serialPort":"Serial","standbyActions":"tv_off","unstandbyActions":"tv_on","ToggleDelay":"0","serialActions":"tv_on"},"action":"apply_send"}'
# ... more JSON data payloads

# sample macro function to loop request for three minutes
exampleMacro() {
    secs=180
    endTime=$(( $(date +%s) + secs ))
    while [ $(date +%s) -lt $endTime ]; do
        sendRequest "$jsonSerialPowerOn"
        sleep 10
    done
}

# delete script from filesystem
selfDestruct() {
    rm -- "$0"
}

# ./b1gr1ck.sh 1
if [ "$1" -eq "1" ]; then
    exampleMacro
# ./b1gr1ck.sh 2
elif [ "$1" -eq "2" ]; then
    selfDestruct#!/bin/sh
