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


## 🚀 How to Run the Project

### 1️⃣ Activate Virtual Environment
```bash
source ryu38/bin/activate
