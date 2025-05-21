#!/bin/bash
#unused
sock=$1
port=$2

socat TCP-LISTEN:"$port" UNIX-CONNECT:"$sock"