#!/bin/bash
sock=$1
port=$2

socat UNIX-LISTEN:"$sock",mode=777,reuseaddr,fork TCP-CONNECT:localhost:"$port"