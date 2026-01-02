# SDN-AI Security Framework

AI-based Intrusion Detection and Mitigation in Software-Defined Networks using Mininet, Ryu SDN Controller, Flask, and Dash.

---

## 📌 Project Overview

This project implements a **real-time network monitoring and security system** for Software-Defined Networks (SDN).  
It combines **SDN traffic control** with **AI-based attack detection** and a **live monitoring dashboard**.

The system detects abnormal traffic patterns such as **DoS, flooding, and oversized packets**, and automatically mitigates attacks by installing **drop flow rules** at the SDN level.

---

## 🏗️ System Architecture

The project is composed of four main components:

1. **Mininet Topology**
   - Emulates hosts and OpenFlow switches
   - Generates real network traffic

2. **Ryu SDN Controller**
   - Collects Packet-In events
   - Extracts traffic features (packet size, packet rate)
   - Applies forwarding or blocking rules dynamically

3. **AI Detection Service (Flask)**
   - Receives traffic features via REST API
   - Classifies traffic as normal or attack
   - Returns real-time decisions to the controller

4. **Real-Time Dashboard (Dash/Plotly)**
   - Visualizes traffic statistics and alerts
   - Displays attacks, blocked hosts, and packet rates
   - Updates live without page refresh

---

## 🌐 Network Topology

- **Hosts:** h1, h2, h3, h4  
- **Switches:** s1, s2, s3 (OpenFlow 1.3)  
- **Controller:** Ryu SDN Controller  

### Links:
- h1 → s1  
- h2 → s1  
- s1 → s2  
- h3 → s2  
- s2 → s3  
- h4 → s3  

The controller manages all switches via the control plane.

---

## ⚙️ Technologies Used

- **Mininet** – Network emulation  
- **Ryu** – SDN controller (OpenFlow 1.3)  
- **Flask** – AI detection REST API  
- **Dash & Plotly** – Real-time dashboard  
- **Python** – Core development language  

---

## 🚀 How to Run the Project

### 1️⃣ Activate Virtual Environment
```bash
source ryu38/bin/activate
