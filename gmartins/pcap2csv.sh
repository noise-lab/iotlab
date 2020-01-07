#/bin/bash

if [ -z "$1" ]
  then
    echo "usage: $BASH_SOURCE example.pcap"
    exit 1
fi

echo "Generating $1.csv..."

tshark -r $1 -T fields -e frame.number -e frame.time -e frame.time_delta -e frame.time_relative -e eth.src_resolved -e eth.dst_resolved -e eth.src -e eth.dst -e eth.type -e ip.version -e ip.hdr_len -e ip.len -e ip.id -e ip.flags.df -e ip.flags.mf -e ip.flags.rb -e ip.flags.sf -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.tos -e ip.ttl -e ip.proto -e ip.src -e ip.dst -e udp.srcport -e udp.dstport -e udp.length -e tcp.flags.cwr -e tcp.flags.ecn -e tcp.flags.urg -e tcp.flags.ack -e tcp.flags.push -e tcp.flags.reset -e tcp.flags.syn -e tcp.flags.fin -e tcp.flags.res -e tcp.flags.ns -e tcp.payload -e tcp.len -e frame.len -E header=y -E separator=\| > $1.csv
