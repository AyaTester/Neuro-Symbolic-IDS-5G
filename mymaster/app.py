import streamlit as st
from neo4j import GraphDatabase
from streamlit_agraph import agraph, Node, Edge, Config
from fpdf import FPDF
import pandas as pd

# --- 1. إعدادات الاتصال وقاعدة البيانات ---
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "Asdfqwer@1234#") 

st.set_page_config(page_title="Neuro-Symbolic IDS Dashboard", layout="wide")

# --- 2. دالة جلب التنبيهات من Neo4j ---
def get_alerts():
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        with driver.session() as session:
            query = """
            MATCH (n:IP)-[r:COMMUNICATES]->(m:IP)
            WHERE r.attack_type <> 'Normal'
            RETURN n.address AS Attacker, 
                   r.attack_type AS Type, 
                   r.packet_rate AS Rate, 
                   r.service AS Service
            ORDER BY r.packet_rate DESC LIMIT 20
            """
            return session.run(query).data()
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return []

# --- 3. دالة إنشاء تقرير PDF آمنة ---
def create_pdf(alerts_data):
    pdf = FPDF()
    pdf.add_page()
    
    # رأس التقرير
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Neuro-Symbolic IDS Security Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Faculty of Computers and Artificial Intelligence - Helwan University", ln=True, align='C')
    pdf.ln(10)

    # جداول العناوين
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Attacker IP", 1)
    pdf.cell(40, 10, "Attack Type", 1)
    pdf.cell(30, 10, "Packet Rate", 1)
    pdf.cell(80, 10, "Symbolic Explanation", 1)
    pdf.ln()

    # محتوى الجدول
    pdf.set_font("Arial", size=9)
    for alert in alerts_data:
        attacker = str(alert.get('Attacker', 'Unknown'))
        attack_type = str(alert.get('Type', 'N/A'))
        
        # معالجة الرقم بشكل آمن
        rate_val = alert.get('Rate')
        rate_text = f"{rate_val:.2f}" if isinstance(rate_val, (int, float)) else "0.00"
        
        service = str(alert.get('Service', 'Network'))
        explanation = f"Anomaly detected via {service} protocol logic."

        pdf.cell(40, 10, attacker, 1)
        pdf.cell(40, 10, attack_type, 1)
        pdf.cell(30, 10, rate_text, 1)
        pdf.cell(80, 10, explanation, 1)
        pdf.ln()

    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 4. دالة بناء بيانات الجراف التفاعلي ---
def load_graph_data():
    nodes = []
    edges = []
    added_nodes = set()
    
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        with driver.session() as session:
            query = """
            MATCH (n:IP)-[r:COMMUNICATES]->(m:IP)
            WHERE r.attack_type <> 'Normal'
            RETURN n, r, m LIMIT 30
            """
            results = session.run(query)
            for record in results:
                src_ip = record['n']['address']
                dst_ip = record['m']['address']
                
                if src_ip not in added_nodes:
                    nodes.append(Node(id=src_ip, label=src_ip, size=30, color="#FF4B4B")) # أحمر للمهاجم
                    added_nodes.add(src_ip)
                
                if dst_ip not in added_nodes:
                    nodes.append(Node(id=dst_ip, label=dst_ip, size=25, color="#1C83E1")) # أزرق للضحية
                    added_nodes.add(dst_ip)
                    
                edges.append(Edge(source=src_ip, target=dst_ip, label=record['r']['attack_type']))
        return nodes, edges
    except:
        return [], []

# --- 5. واجهة المستخدم (UI Layout) ---
st.title("🛡️ Neuro-Symbolic XAI IDS Dashboard")
st.markdown("---")

# القائمة الجانبية
st.sidebar.header("System Controls")
if st.sidebar.button("Refresh Data"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("Reporting")
if st.sidebar.button("Prepare PDF Report"):
    alerts = get_alerts()
    if alerts:
        pdf_bytes = create_pdf(alerts)
        st.sidebar.download_button(
            label="📩 Download PDF Report",
            data=pdf_bytes,
            file_name="Security_Report.pdf",
            mime="application/pdf"
        )
    else:
        st.sidebar.warning("No data to report.")

# تخطيط الصفحة الرئيسي
col_graph, col_info = st.columns([2, 1])

with col_graph:
    st.subheader("Interactive Attack Map")
    nodes, edges = load_graph_data()
    
    if nodes:
        config = Config(
            width=900, height=700, directed=True, physics=True, 
            nodeHighlightBehavior=True, highlightColor="#F7A7A6",
            node={'labelProperty': 'label'},
            link={'labelProperty': 'label', 'renderConfiguration': True}
        )
        return_value = agraph(nodes=nodes, edges=edges, config=config)
    else:
        st.info("Waiting for Neo4j data... ensure the database is running.")

with col_info:
    st.subheader("Symbolic Reasoning Analysis")
    if 'return_value' in locals() and return_value:
        st.success(f"Selected Entity: {return_value}")
        driver = GraphDatabase.driver(URI, auth=AUTH)
        with driver.session() as session:
            res = session.run("MATCH (n:IP {address: $addr})-[r]->(m) RETURN r LIMIT 1", addr=return_value).single()
            if res:
                st.write(f"**GNN Classification:** {res['r']['attack_type']}")
                st.write(f"**Measured Packet Rate:** {res['r']['packet_rate']} p/s")
                st.info(f"**Symbolic Logic:** The security rules validated the anomaly on protocol {res['r']['service']}.")
    else:
        st.write("Click on a network node to retrieve deep symbolic insights.")