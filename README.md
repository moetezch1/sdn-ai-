# SDN-AI Security Framework

AI-based Intrusion Detection and Mitigation in Software-Defined Networks using Mininet, Ryu SDN Controller, Flask, and Dash.

---

## 📌 Project Overview

This project implements a **real-time network monitoring and security system** for Software-Defined Networks (SDN).  
It combines **SDN traffic control**, **AI-based attack detection**, and a **live monitoring dashboard**.

The system detects abnormal traffic patterns such as **DoS attacks, traffic flooding, and oversized packets**, and automatically mitigates threats by installing **drop flow rules** directly on OpenFlow switches.

---

## 🏗️ System Architecture

The system is composed of four main components:

### 1. Mininet Topology
- Emulates a realistic SDN network
- Hosts and OpenFlow switches
- Generates live traffic for analysis

### 2. Ryu SDN Controller
- Handles Packet-In events
- Extracts traffic features (packet size, packet rate)
- Applies forwarding or blocking rules dynamically

### 3. AI Detection Service (Flask)
- Exposes a REST API for traffic classification
- Detects abnormal behavior based on traffic features
- Returns attack decisions to the controller

### 4. Real-Time Dashboard (Dash / Plotly)
- Displays live traffic statistics
- Visualizes attacks and blocked hosts
- Shows packet rates and security events in real time

---

## 🌐 Network Topology

### Nodes
- **Hosts:** h1, h2, h3, h4  
- **Switches:** s1, s2, s3 (OpenFlow 1.3)  
- **Controller:** Ryu SDN Controller  

### Links
- h1 → s1  
- h2 → s1  
- s1 → s2  
- h3 → s2  
- s2 → s3  
- h4 → s3  

The controller manages all switches through the SDN control plane.

---

## 📁 Project Structure

```text
sdn-ai-project/
├── topo.py              # Mininet topology definition
├── sdn_controller.py    # Ryu SDN controller logic
├── ai_detection.py      # AI-based traffic classification service
├── dashboard.py         # Real-time monitoring dashboard
├── README.md            # Project documentation
```

## 🚀 How to Run the Project

### 1️⃣ Activate Virtual Environment
```bash
source ryu38/bin/activate
```

### 2️⃣ Start the AI Detection Service
```bash
source ryu38/bin/activatepython3 ai_detection.py
```
```Runs on:
[source ryu38/bin/activatepython3 ai_detection.py](http://127.0.0.1:5000
)
```


### 3️⃣ Start the Dashboard
```bash
python3 dashboard.py
```
```Runs on:
http://127.0.0.1:8050
```


### 4️⃣ Start the Ryu Controller
```bash
ryu-manager sdn_controller.py
```

### 5️⃣ Launch the Mininet Topology
```bash
sudo python3 topo.py
```

## 📊 Dashboard Features

- Packet rate per MAC address
- Traffic status (Forwarded / Attack / Blocked
- Blocked hosts visualization
- Live security event logs
- Real-time updates (1-second refresh)

## 🔐 Attack Detection Logic

- Traffic is classified as malicious if one or more conditions are met:
- Packet size exceeds the defined threshold
- Packet rate exceeds packets-per-second limit
- AI detection service confirms abnormal behavior


### Mitigation Actions

- Malicious MAC addresses are blocked
- Drop flow rules are installed on switches
- Blocks automatically expire after a timeout

## 🎯 Use Cases

- SDN security experimentation
- Network monitoring systems
- DevOps and NOC dashboards
- AI-assisted traffic analysis
- Academic and engineering projects

## 🔮 Future Improvements

- Advanced ML models (Isolation Forest, LSTM)
- Persistent database for event storage
- User authentication and role management
- Email and webhook alerting
- Support for larger and multi-site topologies


## 👨‍💻 Author

Moetez Chaouch
Telecommunications & Intelligent Systems Engineering
Interests: SDN, AI, Network Security

## 📄 License

This project is intended for educational and research purposes.
