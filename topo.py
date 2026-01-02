from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel

def run():
    net = Mininet(
        controller=None,
        switch=OVSSwitch,
        autoSetMacs=True,
        autoStaticArp=True
    )

    print("*** Adding Ryu controller")
    net.addController(
        'c0',
        controller=RemoteController,
        ip='127.0.0.1',
        port=6653   # ✅ CORRECT PORT
    )

    print("*** Adding hosts")
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    h4 = net.addHost('h4', ip='10.0.0.4/24')

    print("*** Adding switches (OF13)")
    s1 = net.addSwitch('s1', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', protocols='OpenFlow13')
    s3 = net.addSwitch('s3', protocols='OpenFlow13')

    print("*** Adding links (NO LOOP)")
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(s1, s2)
    net.addLink(h3, s2)
    net.addLink(s2, s3)
    net.addLink(h4, s3)

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
