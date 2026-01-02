from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4, icmp
import time
import requests

AI_URL = "http://127.0.0.1:5000/predict"
DASHBOARD_URL = "http://127.0.0.1:8050/event"

MAX_PACKET_SIZE = 500        # bytes
MAX_PACKETS_PER_SEC = 20     # DoS threshold
BLOCK_TIME = 30              # seconds


class SDNController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.packet_count = {}
        self.blocked_macs = {}

    # ================= TABLE MISS =================
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=0, match=match, instructions=inst)
        datapath.send_msg(mod)
        self.logger.info(f"✅ Table-miss installed on switch {datapath.id}")

    # ================= PACKET HANDLER =================
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        if eth is None:
            return

        src_mac = eth.src
        pkt_size = len(msg.data)
        now = time.time()

        # === BLOCKED MAC ===
        if src_mac in self.blocked_macs:
            if now < self.blocked_macs[src_mac]:
                self.logger.warning(f"❌ BLOCKED MAC traffic: {src_mac}")
                self.send_event_to_dashboard(src_mac, pkt_size, "blocked", 0)
                return
            else:
                del self.blocked_macs[src_mac]

        # === PACKET RATE TRACKING ===
        self.packet_count.setdefault(src_mac, [])
        self.packet_count[src_mac].append(now)
        self.packet_count[src_mac] = [t for t in self.packet_count[src_mac] if now - t <= 1]
        pkt_rate = len(self.packet_count[src_mac])

        # === LOCAL RULES ===
        local_attack = (pkt_size > MAX_PACKET_SIZE or pkt_rate > MAX_PACKETS_PER_SEC)

        # === AI DECISION ===
        try:
            response = requests.post(AI_URL, json={"packet_size": pkt_size, "packet_rate": pkt_rate}, timeout=1)
            ai_attack = response.json()["attack"]
        except Exception:
            ai_attack = False

        # === FINAL DECISION ===
        if local_attack or ai_attack:
            self.logger.error(f"❌ ATTACK detected from {src_mac} | size={pkt_size} rate={pkt_rate}")
            self.blocked_macs[src_mac] = now + BLOCK_TIME
            self.install_drop_rule(datapath, src_mac)
            self.send_event_to_dashboard(src_mac, pkt_size, "attack", pkt_rate)
            return

        # === FORWARD ===
        self.logger.info(f"✅ Forwarded packet size={pkt_size} from {src_mac}")
        self.send_event_to_dashboard(src_mac, pkt_size, "forwarded", pkt_rate)

        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
        out = parser.OFPPacketOut(datapath=datapath,
                                  buffer_id=msg.buffer_id,
                                  in_port=msg.match['in_port'],
                                  actions=actions,
                                  data=msg.data)
        datapath.send_msg(out)

    # ================= DROP RULE =================
    def install_drop_rule(self, datapath, src_mac):
        parser = datapath.ofproto_parser
        match = parser.OFPMatch(eth_src=src_mac)
        inst = []

        mod = parser.OFPFlowMod(datapath=datapath,
                                priority=100,
                                match=match,
                                instructions=inst,
                                hard_timeout=BLOCK_TIME)
        datapath.send_msg(mod)
        self.logger.error(f"🚫 DROP rule installed for {src_mac}")

    # ================= DASHBOARD EVENT =================
    def send_event_to_dashboard(self, mac, pkt_size, status, rate):
        try:
            requests.post(DASHBOARD_URL, json={
                "mac": mac,
                "size": pkt_size,
                "status": status,
                "rate": rate,
                "time": time.time()
            }, timeout=0.5)
        except Exception:
            pass
