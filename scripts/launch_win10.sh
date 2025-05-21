#!/bin/bash

monitor_sock=$1
disk_file="$imgdir/desktopwin10.qcow2"
uefi_file="$imgdir/OVMF.4m.fd.win10.qcow2"

qemu-system-x86_64 \
    -boot menu=on \
    -drive file="$disk_file",format=qcow2 \
    -drive if=pflash,format=qcow2,file=$uefi_file \
    -accel kvm -m 16G \
    -smp cores=4,threads=2,sockets=1,maxcpus=8 \
    -cpu host \
    -monitor unix:$monitor_sock,server,nowait \
    -nic user,hostfwd=tcp::1337-:1337 
#    -snapshot