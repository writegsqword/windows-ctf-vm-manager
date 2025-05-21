#!/bin/bash
set -e


export workingdir=$1
export imgdir=$2
export monitor_sock=$3
export forward_sock=$4

ip link set dev lo up
trap 'bash cleanup.sh; kill $(jobs -p)' EXIT

#echo 'loading vm'

bash launch_win10.sh $3 &
#sleep 3

#echo 'loading snapshot'
#bash load_snapshot.sh ready

#echo 'done. vm should be loaded completely now'

nsport=1337

#echo "forwarding $nsport to "$workingdir/forward.sock"
bash expose_privside.sh $forward_sock "$nsport"