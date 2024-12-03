from mininet.net import Mininet
from mininet.node import RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def network():

    net = Mininet(topo=None)
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='127.0.0.1',
                           protocol='tcp',
                           port=6633)

    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')

    info('***Creating hosts\n')

    h1 = net.addHost('h1', ip='192.168.1.1', mac="00:00:00:00:11:00")
    h2 = net.addHost('h2', ip='192.168.1.2', mac="00:00:00:00:22:00")

    info('***Pairing links\n')

    net.addLink(h1, s1)
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, s4)
    net.addLink(s3, s4)
    net.addLink(s4, h2)

    net.build()
    for controller in net.controllers:
        controller.start()

    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])

    CLI(net)
    net.stop()


if '__main__':
    setLogLevel('info')
    network()
