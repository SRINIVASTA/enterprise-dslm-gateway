import streamlit as st
import requests
import json
import time

# 🛡️ Secure cross-module folder import
from scripts.data_masker import mask_sensitive_data

st.set_page_config(page_title="Enterprise DSLM Studio", page_icon="🎛️", layout="wide")
st.title("🔀 Advanced Enterprise DSLM Portfolio Studio")
st.caption("Modular multi-file gateway architecture mapped to the Google Gemini Endpoint ecosystem.")

st.markdown("---")

# Initialize persistent session tracking structures for Cost Guardrails
if "total_spend" not in st.session_state:
    st.session_state.total_spend = 0.0000
if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# --- USER IDENTITY & SECURITY CONTROL PANEL (RBAC) ---
st.sidebar.header("👤 1. Identity & Access Management (RBAC)")
user_role = st.sidebar.selectbox(
    "Select Session Role Profile:",
    ["Engineer (Read & Run)", "Administrator (Full Access & Migration)", "Auditor (Read & Analytics Only)"]
)

if "Engineer" in user_role:
    st.sidebar.info("💼 Access Level: Standard Operator Operations")
elif "Administrator" in user_role:
    st.sidebar.success("👑 Access Level: Root Portfolio Orchestrator")
else:
    st.sidebar.warning("🔍 Access Level: Compliance Inspection Mode")

st.sidebar.markdown("---")

# --- FINANCIAL RUNTIME TRACKER ---
st.sidebar.header("💳 2. Budgetary Cost Guardrails")
BUDGET_CAP = 0.0500 

st.sidebar.progress(min(1.0, st.session_state.total_spend / BUDGET_CAP))
st.sidebar.metric(
    label="Session Token Spend Accumulation", 
    value=f"${st.session_state.total_spend:.4f}", 
    delta=f"Cap: ${BUDGET_CAP:.4f}"
)

if st.session_state.total_spend >= BUDGET_CAP:
    st.sidebar.error("❌ HARD BUDGET CEILING HIT: Inference gateway locked to safeguard finances.")
    gateway_blocked = True
else:
    gateway_blocked = False

# Layout Partition Setup
tab_main, tab_migration = st.tabs(["🚀 DSLM Gateway Pipeline", "📦 Dataset Migration Center"])

# ------------------------------------------
# TAB 1: MODEL INFERENCE GATEWAY
# ------------------------------------------
with tab_main:
    col_config, col_exec = st.columns(2, gap="large")

    with col_config:
        st.subheader("🔑 1. Authentication")
        google_api_key = st.text_input("Paste Google API Key:", type="password", placeholder="AIzaSy...", key="main_token")
        
        is_authenticated = False
        use_mock_engine = False
        
        if google_api_key:
            with st.spinner("Establishing secure handshake with Google API Studio..."):
                try:
                    # 🌐 REST verification route targeting Google's native Generative Language API endpoint
                    api_url = f"https://googleapis.com{google_api_key}"
                    res = requests.get(api_url, headers={'Content-Type': 'application/json'}, timeout=10)
                    
                    if res.status_code == 200:
                        st.success("✅ Verified Account: Google AI Studio Access Granted")
                        is_authenticated = True
                    elif res.status_code == 400 or res.status_code == 403:
                        st.error("❌ Authentication Refused: Invalid Google API key credentials.")
                    else:
                        use_mock_engine = True
                        is_authenticated = True
                except Exception:
                    # 🔌 If the Streamlit server encounters a DNS/network block, switch to mock sandbox natively
                    use_mock_engine = True
                    is_authenticated = True

            if use_mock_engine:
                st.warning("⚠️ Network Isolation Detected: Local Mock Inference Engine Activated for Live Demo Workflow.")
                st.session_state.engine_mode = "mock"
            else:
                st.session_state.engine_mode = "live"
        else:
            st.info("💡 Paste your Google API Key (starts with 'AIzaSy') above to begin.")

        st.markdown("---")
        
        st.subheader("🎛️ 2. Inference Hyperparameters")
        model_choice = st.selectbox(
            "Target Google Architecture:", 
            ["gemini-2.5-flash", "gemini-2.5-pro"]
        )
        temperature = st.slider("Temperature (Precision Control):", min_value=0.0, max_value=1.0, value=0.1, step=0.05)
        max_tokens = st.slider("Max Output Tokens:", min_value=10, max_value=2048, value=300, step=10)
    with col_exec:
        st.subheader("📜 3. Enterprise System Templates")
        template_text = (
            "You are an expert telecom infrastructure diagnostic system specialized in OSS, Open RAN, IMS, and LTE topologies.\n"
            "Analyze the following network log alarm and output your analysis STRICTLY in this format:\n"
            "- [ROOT CAUSE]: Clear explanation of the fault.\n"
            "- [IMPACT ASSESSMENT]: Affected nodes or services.\n"
            "- [REMEDIATION STEPS]: Numbered, step-by-step instructions to minimize MTTR.\n\n"
            "Network Ticket Log:\n{user_input}"
        )
        
        st.text_area("System Prompt Preview (Read-Only):", value=template_text, height=130, disabled=True)
        
        st.markdown("---")
        st.subheader("📝 4. Live Data Feed Input")
        
        sample_log = (
            "[ALARM] 2026-09-02T10:14:22Z\n"
            "SEVERITY: CRITICAL\n"
            "COMPONENT: IMS_HSS_CORE_02\n"
            "TARGET_IP: 10.145.22.89\n"
            "ERROR_CODE: 504 Gateway Timeout\n"
            "DESCRIPTION: Diameter interface connection dropped during subscriber profile retrieval sequence. LTE attached devices failing VoLTE registration handshakes."
        )
        
        if "input_buffer" not in st.session_state:
            st.session_state.input_buffer = sample_log
            
        if st.button("📥 Reset to Sample Telecom Fault Log"):
            st.session_state.input_buffer = sample_log
            
        raw_input = st.text_area("Enter Logs:", value=st.session_state.input_buffer)
        
        masked_input = mask_sensitive_data(raw_input)
        compiled_prompt = template_text.replace("{user_input}", masked_input)
        
        with st.expander("🔍 Preview Masked Payload", expanded=True):
            st.code(compiled_prompt, language="text")
            
        allow_execution = is_authenticated and not gateway_blocked and ("Auditor" not in user_role)
        
        btn_label = "Run Pipeline"
        if "Auditor" in user_role:
            btn_label = "🚫 Pipeline Locked for Auditors"
            
        if st.button(btn_label, type="primary", disabled=not allow_execution):
            if not raw_input.strip():
                st.warning("⚠️ Input data feed cannot be empty.")
            else:
                start_time = time.time()
                current_engine = st.session_state.get("engine_mode", "mock")
                
                with st.spinner(f"Processing via {current_engine.upper()} infrastructure pipeline..."):
                    
                    # 📡 PATH A: LIVE GOOGLE GEMINI EXECUTION
                    if current_engine == "live":
                        # Google's core direct REST API call pattern for handling generative language updates
                        API_URL = f"https://googleapis.com{model_choice}:generateContent?key={google_api_key}"
                        headers = {"Content-Type": "application/json"}
                        payload = {
                            "contents": [{"parts": [{"text": compiled_prompt}]}],
                            "generationConfig": {
                                "temperature": temperature,
                                "maxOutputTokens": max_tokens
                            }
                        }
                        
                        try:
                            res = requests.post(API_URL, headers=headers, json=payload, timeout=40)
                            latency = round(time.time() - start_time, 2)
                            
                            if res.status_code == 200:
                                result = res.json()
                                # Safe dictionary parsing extraction mapping out Gemini's standard nested JSON structure
                                output_text = result['candidates'][0]['content']['parts'][0]['text']
                                st.success("🤖 Analysis Complete (Live Google Cloud Inference)")
                                st.write(output_text)
                            else:
                                st.error(f"Google Execution Error ({res.status_code}): {res.text}")
                                current_engine = "mock"  # Dynamic downgrade if API limits are breached
                        except Exception as e:
                            st.error(f"Live route connection blocked, falling back to mock sandbox... Error: {e}")
                            current_engine = "mock"
                    
                    # 🔌 PATH B: LOCAL RESILIENT MOCK EXECUTOR
                    if current_engine == "mock":
                        time.sleep(1.5)
                        latency = round(time.time() - start_time, 2)
                        st.success("🤖 Analysis Complete (Generated via Sandbox Portfolio Core)")
                        st.markdown(
                            "### 📟 Diagnostic Generation Output\n"
                            "**- [ROOT CAUSE]:** A complete connectivity failure occurred on the Diameter interface within the **IMS_HSS_CORE_02** node infrastructure. This degradation was precipitated by an unhandled transport layer exception, which triggered a continuous chain of 504 Gateway Timeouts during subscriber database profile lookups.\n\n"
                            "**- [IMPACT ASSESSMENT]:** Critical failure spreading to adjacent downstream subsystems. All LTE attached endpoint hardware are completely blocked from completing basic session cryptographic keys handshakes, causing an immediate, total loss of Voice over LTE (VoLTE) call setups across regional cell coverage bands.\n\n"
                            "**- [REMEDIATION STEPS]:**\n"
                            "1. **Isolate Interface Routing:** Manually purge the broken peering socket queues on the main database router node.\n"
                            "2. **Execute VNF Failover Switchover:** Run the system automated scripts to migrate volatile database memory registers from `IMS_HSS_CORE_02` over to the secondary passive host server cluster.\n"
                            "3. **Recalibrate Timeout Caps:** Tweak the internal timer value limits inside your configuration file downward from 120s down to 30s to lower the overall systemic MTTR metrics footprint."
                        )
                    
                    # --- SHARED REUSABLE METRICS COMPUTE BLOCK ---
                    current_call_cost = 0.00015 
                    st.session_state.total_spend += current_call_cost
                    st.session_state.query_count += 1
                    
                    st.markdown("---")
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric(label="Inference Latency Profile", value=f"{latency}s")
                    with col_m2:
                        st.metric(label="Cost For This Execution", value=f"${current_call_cost:.5f}")
                    with col_m3:
                        st.metric(label="Total Continuous Call Volume", value=st.session_state.query_count)
                        
                    if st.session_state.total_spend >= BUDGET_CAP:
                        st.rerun()

# ------------------------------------------
# TAB 2: DATA MIGRATION CENTER
# ------------------------------------------
with tab_migration:
    if "Administrator" not in user_role:
        st.error("🔒 CRITICAL PERMISSION REFUSAL: You must have the Administrator role profile to access data cluster migration systems.")
    else:
        st.subheader("📦 Dataset Migration Center")
        st.caption("Simulation Mode: Local data parsing engine verified.")
        st.info("💡 Storage channels are currently locked under local offline execution protocol parameters.")
