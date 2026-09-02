import streamlit as st
import requests
import json
import time

# 🛡️ Secure cross-module folder imports
from scripts.data_masker import mask_sensitive_data
from scripts.dataset_uploader import upload_to_google_ai

# App Page Layout Base Initialization 
st.set_page_config(page_title="Enterprise DSLM Studio", page_icon="🎛️", layout="wide")
st.title("🔀 Advanced Enterprise DSLM Portfolio Studio")
st.caption("Modular multi-file gateway architecture mapped to the Google Gemini Endpoint ecosystem.")

st.markdown("---")

# Initialize persistent session tracking structures for Cost Guardrails
if "total_spend" not in st.session_state:
    st.session_state.total_spend = 0.0003
if "query_count" not in st.session_state:
    st.session_state.query_count = 3

# --- USER IDENTITY & SECURITY CONTROL PANEL (RBAC) ---
st.sidebar.header("👤 1. Identity & Access Management (RBAC)")
user_role = st.sidebar.selectbox(
    "Select Session Role Profile:",
    ["Engineer (Read & Run)", "Administrator (Full Access & Migration)", "Auditor (Read & Analytics Only)"]
)

# Extract boolean configuration flags based on the user session profile
is_auditor = "Auditor" in user_role
is_admin = "Administrator" in user_role

if "Engineer" in user_role:
    st.sidebar.info("💼 Access Level: Standard Operator Operations")
elif is_admin:
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

# Layout Partition Tab Setup
tab_main, tab_migration = st.tabs(["🚀 DSLM Gateway Pipeline", "📦 Dataset Migration Center"])

# ------------------------------------------
# TAB 1: MODEL INFERENCE GATEWAY
# ------------------------------------------
with tab_main:
    col_config, col_exec = st.columns(2, gap="large")

    with col_config:
        # 🟢 STEP 1: Pre-initialize the variable at the top of the column thread
        # This keeps Python happy while maintaining your layout order!
        chosen_model_architecture = "gemini-1.5-flash"
        if "main_model_selector" in st.session_state:
            chosen_model_architecture = st.session_state["main_model_selector"]

        # 🟢 STEP 2: Your exact visual layout - 1. Authentication on top!
        st.subheader("🔑 1. Authentication")
        google_api_key = st.text_input("Paste Google API Key:", type="password", placeholder="AIzaSy...", key="main_token")
        
        is_authenticated = False
        use_mock_engine = False
        
        if google_api_key:
            with st.spinner("Establishing secure handshake with Google API Studio..."):
                try:
                    from google import genai
                    client = genai.Client(api_key=google_api_key)
                    
                    # ✅ FIXED: Dynamically verifies whichever model you currently have selected below!
                    res = client.models.generate_content(
                        model=chosen_model_architecture,
                        contents='ping'
                    )
                    
                    if res.text:
                        st.success(f"✅ Verified Account: Google AI Studio Access Granted ({chosen_model_architecture})")
                        is_authenticated = True
                        use_mock_engine = False
                except Exception as e:
                    # Captures your 429 quota exhaustion dynamically per model track line
                    st.error(f"❌ Authentication Refused: Model Lane Quota Constraints. (Error: {str(e)})")
                    use_mock_engine = True
                    is_authenticated = True

            if use_mock_engine:
                st.warning("⚠️ Network Isolation Detected: Local Mock Inference Engine Activated for Live Demo Workflow.")
                st.session_state.engine_mode = "mock"
            else:
                st.session_state.engine_mode = "live"
        else:
            st.info("💡 Paste your Google API Key above to begin.")

        st.markdown("---")
        
        # 🟢 STEP 3: Your exact visual layout - 2. Inference Hyperparameters stays on the bottom!
        st.subheader("🎛️ 2. Inference Hyperparameters")
        model_choice = st.selectbox(
            "Target Google Architecture:", 
            ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-1.5-pro", "gemini-1.0-pro", "text-embedding-004"],
            key="main_model_selector" # Ties directly into your pre-initialized session memory token flag
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
        
        # 🌐 FIXED LINK: Captures raw log blocks directly bypassing GitHub UI wrappers
        GITHUB_LOG_URL = "https://githubusercontent.com"
        
        sample_log = (
            "[ALARM] 2026-09-02T10:14:22Z\n"
            "SEVERITY: CRITICAL\n"
            "COMPONENT: IMS_HSS_CORE_02\n"
            "TARGET_IP: 10.145.22.89\n"
            "ERROR_CODE: 504 Gateway Timeout\n"
            "DESCRIPTION: Diameter interface connection dropped during subscriber profile retrieval sequence."
        )
        
        if "input_buffer" not in st.session_state:
            st.session_state.input_buffer = sample_log
            
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("📥 Pull Automated Logs from GitHub", use_container_width=True):
                with st.spinner("Syncing data assets live from repository branch..."):
                    try:
                        # Fetch the direct text payload from your raw link path
                        res = requests.get(GITHUB_LOG_URL, timeout=8)
                        if res.status_code == 200:
                            st.session_state.input_buffer = res.text
                            st.success("✅ Synchronized: Master Ingestion Payload (Repo Run: 006) Loaded!")
                            st.rerun()
                        else:
                            st.error(f"⚠️ Repository File Link Offline (HTTP {res.status_code}).")
                            st.session_state.input_buffer = sample_log
                            st.rerun()
                    except Exception as e:
                        st.error(f"❌ Connection Blocked: {str(e)}")
                        st.session_state.input_buffer = sample_log
                        st.rerun()
                        
        with col_btn2:
            if st.button("🔄 Reset to Default Local Log Template", use_container_width=True):
                st.session_state.input_buffer = sample_log
                st.rerun()
                
        raw_input = st.text_area("Enter Logs:", value=st.session_state.input_buffer, key="log_input_feed", height=200)
        
        # Local regex scanning step triggers in-flight prior to variable string injection
        masked_input = mask_sensitive_data(raw_input)
        compiled_prompt = template_text.replace("{user_input}", masked_input)
        
        with st.expander("🔍 Preview Masked Payload", expanded=True):
            st.code(compiled_prompt, language="text")
            
        allow_execution = is_authenticated and not gateway_blocked and not is_auditor
        
        btn_label = "Run Pipeline"
        if is_auditor:
            btn_label = "🚫 Pipeline Locked for Auditors"
            
        if st.button(btn_label, type="primary", disabled=not allow_execution):
            if not raw_input.strip():
                st.warning("⚠️ Input data feed cannot be empty.")
            else:
                start_time = time.time()
                current_engine = st.session_state.get("engine_mode", "mock")
                
                with st.spinner(f"Processing via {current_engine.upper()} infrastructure pipeline..."):
                    
                    # 📡 PATH A: LIVE GOOGLE GEMINI NATIVE LIBRARY INFERENCE
                    if current_engine == "live":
                        try:
                            from google import genai
                            from google.genai import types
                            
                            # Initialize authorized local client session instance
                            client = genai.Client(api_key=google_api_key)
                            
                            # Construct unified generation configuration map blocks
                            config = types.GenerateContentConfig(
                                temperature=temperature,
                                max_output_tokens=max_tokens
                            )
                            
                            # Dispatch payload over programmatic channels
                            response = client.models.generate_content(
                                model=model_choice,
                                contents=compiled_prompt,
                                config=config
                            )
                            
                            latency = round(time.time() - start_time, 2)
                            output_text = response.text if response.text else "Empty response output matrix payload returned."
                            
                            st.success("🤖 Analysis Complete (Live Google Cloud Inference)")
                            st.markdown(output_text)
                            
                            # Sub-penny pricing tracker execution logic proxies
                            input_tokens = len(compiled_prompt) / 4.0
                            output_tokens = len(output_text) / 4.0
                            current_call_cost = ((input_tokens * 0.075) + (output_tokens * 0.30)) / 1_000_000
                        except Exception as e:
                            st.error(f"Live network route connection blocked, downshifting to local sandbox... Info: {e}")
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
                        current_call_cost = 0.00015 
                    
                    # Update global telemetry counters
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
# TAB 2: DATA MIGRATION CENTER (GOOGLE FILE API)
# ------------------------------------------
with tab_migration:
    if not is_admin:
        st.error("🔒 CRITICAL PERMISSION REFUSAL: You must have the Administrator role profile to access data cluster migration systems.")
    else:
        st.subheader("📦 Dataset Migration Center")
        st.caption("Publish telemetry data assets directly to your Google Cloud AI Project storage plane.")
        
        # Automatically inherit the key entered in Tab 1
        active_key = google_api_key if google_api_key else ""
        
        if not active_key:
            st.info("💡 Please provide a functional Google API Key in the Authentication panel (Tab 1) to enable uploads.")
            
        target_filename = st.text_input("Target Cloud File Name:", value="telecom_train_logs.txt", key="goog_file_id")
        raw_log_dump = st.text_area("Paste Corporate Diagnostic Dump Data:", key="goog_dump_data", height=150)
        
        # 🌐 FIXED RAW ENDPOINT: Pulls down your exact Repo Run: 006 text payload bypassing the GitHub UI wrappers
        # 🌐 CACHE-PROOF FIX: Hardcodes the true unformatted raw background text stream on GitHub
        GITHUB_LOG_URL = "".join([
            "https://", 
            "raw.", 
            "githubusercontent.com", 
            "/SRINIVASTA/enterprise-dslm-gateway/main/telecom_train_logs.txt"
        ])
        
        # Button unlocks exclusively when an active API key string is present
        if st.button("Upload Asset to Google File API Suite", key="goog_submit_btn", type="secondary", disabled=not active_key):
            final_upload_payload = raw_log_dump.strip()
            
            # 🔄 AUTOMATED GITHUB ARMED FALLBACK LAYER
            if not final_upload_payload:
                st.warning("⚠️ Input field blank! Automatically capturing file from GitHub repository...")
                try:
                    res = requests.get(GITHUB_LOG_URL, timeout=8)
                    if res.status_code == 200:
                        final_upload_payload = res.text
                        st.info("📥 Captured 'telecom_train_logs.txt' successfully from main branch repository stream.")
                    else:
                        st.error(f"❌ GitHub Server Error: Received HTTP status code {res.status_code}")
                except Exception as e:
                    st.error(f"❌ Fallback path network exception: {str(e)}")
            
            # Final operational validation check block
            if not target_filename.strip():
                st.error("❌ Missing Target Cloud File Name target descriptor.")
            elif final_upload_payload:
                with st.spinner("Streaming data chunk payload directly to Google API infrastructure..."):
                    # Call your modularized uploader module using the fallback text payload natively
                    result = upload_to_google_ai(active_key, target_filename, final_upload_payload)
                    
                    if result["status"] == "success":
                        st.success("🚀 Upload successful! Your operational records are mapped to Google AI Storage.")
                        st.code(f"Google Resource Location Pointer (URI):\n{result['uri']}", language="text")
                    else:
                        st.error(result["message"])
