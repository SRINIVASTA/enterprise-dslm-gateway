import streamlit as st
import requests
import json
import time

# 🛡️ Secure folder import
from scripts.data_masker import mask_sensitive_data

st.set_page_config(page_title="Enterprise DSLM Studio", page_icon="🎛️", layout="wide")
st.title("🔀 Advanced Enterprise DSLM Portfolio Studio")
st.caption("Modular multi-file gateway architecture deployed directly via GitHub Web & Streamlit Cloud.")

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

# Render role badges
if "Engineer" in user_role:
    st.sidebar.info("💼 Access Level: Standard Operator Operations")
elif "Administrator" in user_role:
    st.sidebar.success("👑 Access Level: Root Portfolio Orchestrator")
else:
    st.sidebar.warning("🔍 Access Level: Compliance Inspection Mode")

st.sidebar.markdown("---")

# --- FINANCIAL RUNTIME TRACKER ---
st.sidebar.header("💳 2. Budgetary Cost Guardrails")
BUDGET_CAP = 0.0500 # Set a hard token ceiling limit for test cycles

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
        hf_token = st.text_input("Paste Hugging Face Token:", type="password", placeholder="hf_...", key="main_token")
        is_authenticated = False
        
        if hf_token:
            with st.spinner("Validating token..."):
                try:
                    res = requests.get(
                        "https://huggingface.co", 
                        headers={"Authorization": f"Bearer {hf_token}"}, 
                        timeout=10
                    )
                    if res.status_code == 200:
                        st.success(f"✅ Verified Account: {res.json().get('name')}")
                        is_authenticated = True
                    else:
                        st.error("❌ Invalid Token. Check your permissions.")
                except Exception:
                    st.error("Validation failed: Connection error.")
        else:
            st.info("💡 Paste your Hugging Face user access token above to begin.")

        st.markdown("---")
        
        st.subheader("🎛️ 2. Inference Hyperparameters")
        model_choice = st.selectbox(
            "Target Model Architecture:", 
            ["mistralai/Mistral-7B-Instruct-v0.3", "meta-llama/Llama-3.1-8B-Instruct", "microsoft/Phi-4"]
        )
        temperature = st.slider("Temperature (Precision Control):", min_value=0.01, max_value=1.5, value=0.1, step=0.05)
        max_tokens = st.slider("Max New Tokens:", min_value=10, max_value=2048, value=300, step=10)

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
            "[ALARM] 2026-09-02T17:45:00 UTC\n"
            "Severity: CRITICAL\n"
            "Fault Code: 403 (Forbidden)\n"
            "Source Element: LTE_VNF_NODE_04\n"
            "Target IP: 192.168.254.45\n"
            "Message: IMS core registration failure. Handshake authentication loop timed out."
        )
        
        if "input_buffer" not in st.session_state:
            st.session_state.input_buffer = ""
            
        if st.button("📥 Load Sample Telecom Fault Log"):
            st.session_state.input_buffer = sample_log
            
        raw_input = st.text_area("Enter Logs:", value=st.session_state.input_buffer)
        
        masked_input = mask_sensitive_data(raw_input)
        compiled_prompt = template_text.replace("{user_input}", masked_input)
        
        with st.expander("🔍 Preview Masked Payload"):
            st.code(compiled_prompt, language="text")
            
        # UI Button state adjustment based on current active security context rules
        allow_execution = is_authenticated and not gateway_blocked and ("Auditor" not in user_role)
        
        btn_label = "Run Pipeline"
        if "Auditor" in user_role:
            btn_label = "🚫 Pipeline Locked for Auditors"
            
        if st.button(btn_label, type="primary", disabled=not allow_execution):
            if not raw_input.strip():
                st.warning("⚠️ Input data feed cannot be empty.")
            else:
                API_URL = f"https://huggingface.co{model_choice}"
                headers = {"Authorization": f"Bearer {hf_token}"}
                payload = {"inputs": compiled_prompt, "parameters": {"temperature": temperature, "max_new_tokens": max_tokens, "return_full_text": False}}
                
                start_time = time.time()
                with st.spinner("Processing through portfolio layer..."):
                    res = requests.post(API_URL, headers=headers, json=payload, timeout=45)
                    latency = round(time.time() - start_time, 2)
                    
                    if res.status_code == 200:
                        result = res.json()
                        output_text = result.get('generated_text', '') if isinstance(result, list) else str(result)
                        
                        st.success("🤖 Analysis Complete")
                        st.write(output_text)
                        
                        # --- DYNAMIC COST CALCULATION ENGINE ---
                        # Small models incur roughly $0.00015 per run benchmark metrics
                        current_call_cost = 0.00015 
                        st.session_state.total_spend += current_call_cost
                        st.session_state.query_count += 1
                        
                        st.markdown("---")
                        col_m1, col_m2, col_m3 = st.columns(3)
                        with col_m1:
                            st.metric(label="Inference Latency", value=f"{latency}s")
                        with col_m2:
                            st.metric(label="Cost For This Execution", value=f"${current_call_cost:.5f}")
                        with col_m3:
                            st.metric(label="Total Continuous Call Volume", value=st.session_state.query_count)
                            
                        # Proactive warning system before next tick trigger
                        if st.session_state.total_spend >= BUDGET_CAP:
                            st.rerun()
                            
                    elif res.status_code == 503:
                        st.warning("⏳ Model waking up in Hugging Face memory. Try again in 15 seconds.")
                    else:
                        st.error(f"Error: {res.text}")

# ------------------------------------------
# TAB 2: DATA MIGRATION CENTER (ADMIN ONLY)
# ------------------------------------------
with tab_migration:
    if "Administrator" not in user_role:
        st.error("🔒 CRITICAL PERMISSION REFUSAL: You must have the Administrator role profile to access data cluster migration systems.")
    else:
        from scripts.dataset_uploader import handle_web_upload
        handle_web_upload()
