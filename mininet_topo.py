#!/usr/bin/python

#Copyright (c) 2016 Enrique Saurez

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys

from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info, warn
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.util import dumpNodeConnections

class customTopo(Topo):
    """create topology with numCore core switches
    numEdge edge switches, hostsPerEdge, bw bandwidth, delay"""
    
    def build(self, numCores = 2, numEdges=3, hostsPerEdge=2, bw = 5, delay = None):

        configuration = dict(bw=bw, delay=delay, max_queue_size=1, loss=0, use_htb=True)

        hosts = [ [self.addHost( 'h%s' % h ) for h in range( e * hostsPerEdge + 1, (e+1) * hostsPerEdge + 1)] for e in range(numEdges) ]
        edges = [ self.addSwitch('c%s' % e, protocols='OpenFlow13')  for e in range( 1, numEdges + 1)]
        cores = [ self.addSwitch('c%s' % c, protocols='OpenFlow13')  for c in range( 1, numCores + 1)]
        
        for core in cores:
            for edge in edges:
                self.addLink(core, edge, **configuration)
    
        for e, edge in enumerate(edges):
            for host in hosts[e]:
                self.addLink(host, edge, **configuration)
            
           
def test():
    ip = '127.0.0.1'
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    
    print "Building topology"
    topo = customTopo()
    net = Mininet(topo=topo, link=TCLink, controller=None)
    

    print "start RYU controller in ip: {}".format(ip)
    raw_input()

    net.addController('rmController', controller=RemoteController,
                      ip=ip, port=6633)
    net.start()

    print "Testing network connectivity"
    net.pingAll()
    #dumpNodeConnections(net.hosts)
    print "Testing bandwidth between h1 and h4"
    h1, h4 = net.get('h1', 'h4')
    net.iperf((h1, h4))
    CLI(net)
    net.stop()
    

if __name__ == '__main__':
    setLogLevel('info')
    test()
