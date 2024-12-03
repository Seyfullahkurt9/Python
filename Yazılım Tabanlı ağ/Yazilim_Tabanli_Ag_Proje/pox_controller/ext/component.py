from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

def do_switch_router(event, packet, packet_in, switch_id):
    if(((str(packet.payload)).find("ARP")==-1)):
        if((((str(packet.payload.srcip)).find("192.168.1.1"))>-1)|(((str(packet.payload.srcip)).find("192.168.1.2"))>-1)):
            print("------------------------------------------------------------------------")
            print(" Kullanilan switch numarasi: ", switch_id, "\n Paketi gonderen kaynagin MAC adresi > Hedefin MAC adresi: \n", packet.src, ">", packet.dst,  "\n Paketi gonderen kaynagin IP adresi > Hedefin IP adresi:\n",  packet.payload.srcip , ">" , packet.payload.dstip)
            print("------------------------------------------------------------------------")
    if switch_id == 1:
        if packet.src == "00:00:00:00:11:00":
            msg = of.ofp_flow_mod()
            msg.data = event.ofp
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 30
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=  2))
            event.connection.send(msg)
        elif packet.src == "00:00:00:00:22:00":
            msg = of.ofp_flow_mod()
            msg.data = event.ofp
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 30
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

    elif switch_id == 2:
        if packet.src == "00:00:00:00:11:00":
            msg = of.ofp_flow_mod()
            msg.data = event.ofp
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 30
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)
        elif packet.src == "00:00:00:00:22:00":
            msg = of.ofp_flow_mod()
            msg.data = event.ofp
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 30
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

    elif switch_id == 3:
        if packet.src == "00:00:00:00:11:00":
            msg = of.ofp_flow_mod()
            msg.data = event.ofp
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 30
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)
        elif packet.src == "00:00:00:00:22:00":
            msg = of.ofp_flow_mod()
            msg.data = event.ofp
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 30
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=1))
            event.connection.send(msg)

    elif switch_id == 4:
        if packet.src == "00:00:00:00:11:00":
            msg = of.ofp_flow_mod()
            msg.data = event.ofp
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 60
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=3))
            event.connection.send(msg)
        elif packet.src == "00:00:00:00:22:00":
            msg = of.ofp_flow_mod()
            msg.data = event.ofp
            msg.match = of.ofp_match.from_packet(packet)
            msg.idle_timeout = 60
            msg.hard_timeout = 60
            msg.actions.append(of.ofp_action_output(port=2))
            event.connection.send(msg)

def _handle_PacketIn(event):
    packet = event.parsed
    packet_in = event.ofp
    switch_id = event.dpid
    do_switch_router(event, packet, packet_in, switch_id)

def start_switch(event):
    #SwitchRouting(event.connection)
    pass

def _handle_UpEvent(event):
    #log.debug("upevent okey")
    pass

def launch():
    core.addListenerByName("UpEvent", _handle_UpEvent)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

