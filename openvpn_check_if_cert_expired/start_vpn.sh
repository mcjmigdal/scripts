#!/bin/sh
expiresAt=`grep "Not After" myusername.crt | cut -d: -f2-10`
if [[ `date -d "${expiresAt}" +%s` < `date +%s` ]]; then
	echo "Certificate has expired!"
	runuser -u myusername firefox url://to/new/certificate &
	exit 2
fi
openvpn --auth-nocache  --cd . --config vpn.conf --daemon --log vpn.log
