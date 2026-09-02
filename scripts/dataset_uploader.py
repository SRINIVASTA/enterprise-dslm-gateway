import streamlit as st

def handle_web_upload():
    """Handles dataset upload UI directly via the Streamlit web environment."""
    st.subheader("📦 Dataset Migration Center")
    st.caption("Publish training files directly to your private Hugging Face account layout.")
    
    mig_token = st.text_input("HF Upload Token:", type="password", key="mig_upload_token")
    target_repo = st.text_input("HF Dataset Repo ID (e.g., org/my-dataset):", key="mig_repo_id")
    raw_jsonl = st.text_area("Paste JSON Lines Data:", key="mig_jsonl_data")
    
    if st.button("Upload to Hugging Face Hub", key="mig_submit_btn"):
        if not mig_token or not target_repo or not raw_jsonl.strip():
            st.error("❌ Missing required configuration fields.")
        else:
            with st.spinner("Uploading text payload directly to Hugging Face..."):
                try:
                    from huggingface_hub import HfApi
                    api = HfApi()
                    api.upload_file(
                        path_or_fileobj=raw_jsonl.encode('utf-8'),
                        path_in_repo="train.jsonl",
                        repo_id=target_repo,
                        repo_type="dataset",
                        token=mig_token
                    )
                    st.success("🚀 Upload successful! Your records are now updated on the Hub.")
                except Exception as e:
                    st.error(f"Upload failed: {e}")
