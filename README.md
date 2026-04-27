# Neuro-Symbolic-IDS-5G
# Neuro-Symbolic IDS for 5G/IoT Security 🛡️🧠

This repository contains the implementation of an **Explainable Artificial Intelligence (XAI)** framework for Intrusion Detection in 5G and IoT networks. The project combines the pattern recognition power of **Graph Neural Networks (GNN)** with the logical reasoning of **Knowledge Graphs (Neo4j)**.

## 🚀 Overview
Traditional AI models for cybersecurity often act as "black boxes." This project implements a **Neuro-Symbolic** approach to provide:
1. **High-Accuracy Detection:** Using GNNs to identify complex attack patterns in network traffic.
2. **Explainability (XAI):** Utilizing Neo4j to provide symbolic reasoning and human-readable explanations for every detected alert.
3. **Temporal Awareness:** Tracking attack propagation over time to address **Concept Drift**.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Deep Learning:** PyTorch / PyTorch Geometric (GNN)
* **Graph Database:** Neo4j (Cypher Query Language)
* **Dashboard:** Streamlit (Interactive Analyst Interface)
* **Dataset:** X-IIoTID (Industrial IoT Dataset)

## 📁 Project Structure
* `to_neo4j.py`: Script to preprocess the dataset and migrate network flows into the Neo4j Knowledge Graph with temporal attributes.
* `app.py`: The Streamlit-based Security Analyst Dashboard for real-time visualization and reasoning.
* `logic_rules.cypher`: (Optional) A collection of symbolic rules for attack validation.

## 📊 Key Features
- **Interactive Attack Graph:** Visualize how an attacker moves through the network.
- **Symbolic Reasoning:** Instead of just a "Malicious" label, the system explains *why* (e.g., "High packet rate on MQTT port + GNN classification = Potential DoS").
- **Temporal Analysis:** Monitor attack frequency and duration to detect evolving threats.

## 🚦 How to Run
1. **Prerequisites:**
   - Install Neo4j Desktop and start a local database.
   - Install Python dependencies:
     ```bash
     pip install streamlit streamlit-agraph neo4j pandas
     ```
2. **Data Migration:**
   - Run `python to_neo4j.py` to populate your Knowledge Graph.
3. **Launch Dashboard:**
   - Run `streamlit run app.py` to open the analyst interface.

## 🎓 Academic Context
This project is part of a Master’s Thesis research at the **Faculty of Computers and Artificial Intelligence, Helwan University**. 
- **Researcher:** Aya Khalifa
- **Supervised by:** Prof. Mahmoud Elkhouly

## 📜 License
This project is for academic purposes. Please cite the repository if you use the code in your research.
