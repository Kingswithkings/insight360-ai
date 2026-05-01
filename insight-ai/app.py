import streamlit as st
from ai_engine import analyze_public_document
from pdf_reader import extract_text_from_pdf
from report_generator import generate_pdf_report


st.set_page_config(
    page_title="Insight AI",
    page_icon="🧠",
    layout="wide"
)


st.title("🧠 Insight AI")
st.caption("Turn complex public information into clear decisions.")
st.info("Insight AI helps simplify complex public documents, policy updates, and reports into clear, structured insights for everyday understanding.")


st.markdown("""
Upload a PDF or paste text below.
""")


st.divider()


uploaded_file = st.file_uploader(
    "Upload public document PDF",
    type=["pdf"]
)

text_input = st.text_area(
    "Or paste document text here",
    height=250,
    placeholder="Paste council update, public statement, policy document, or report text here..."
)


analyze_button = st.button("Analyze Document", type="primary")


if analyze_button:
    if uploaded_file is None and not text_input.strip():
        st.warning("Please upload a PDF or paste text before analyzing.")
        st.stop()

    if uploaded_file is not None:
        with st.spinner("Extracting text from PDF..."):
            document_text = extract_text_from_pdf(uploaded_file)
    else:
        document_text = text_input.strip()

    if not document_text:
        st.error("No readable text found. Please try another document.")
        st.stop()

    with st.spinner("Analyzing document..."):
        result = analyze_public_document(document_text)

    st.success("Analysis complete.")

    st.divider()

    st.subheader("📝 Simple Summary")
    st.write(result.get("simple_summary", "No summary generated."))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📌 Key Decisions")
        key_decisions = result.get("key_decisions", [])
        if key_decisions:
            for item in key_decisions:
                st.write(f"- {item}")
        else:
            st.write("No key decisions identified.")

    with col2:
        st.subheader("⚠️ Risks")
        risks = result.get("risks", [])
        if risks:
            for item in risks:
                st.write(f"- {item}")
        else:
            st.write("No risks identified.")

    st.subheader("📊 Public Impact")
    st.write(result.get("public_impact", "No public impact generated."))

    st.subheader("🏡 What This Means for Residents")
    resident_points = result.get("what_it_means_for_residents", [])
    if resident_points:
        for item in resident_points:
            st.write(f"- {item}")
    else:
        st.write("No resident impact points generated.")

    st.subheader("✅ Recommended Actions")
    actions = result.get("recommended_actions", [])
    if actions:
        for item in actions:
            st.write(f"- {item}")
    else:
        st.write("No recommended actions generated.")

    st.divider()

    pdf_report = generate_pdf_report(result)

    st.download_button(
        label="Download PDF Report",
        data=pdf_report,
        file_name="insight_analysis_report.pdf",
        mime="application/pdf"
    )


st.divider()

st.caption("Insight AI is an early prototype by 1stKings Ltd. Outputs should be reviewed by humans before decision-making.")