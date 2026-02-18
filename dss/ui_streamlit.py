import streamlit as st

from dss.schemas import UserNeeds
from dss.knowledge_base import load_kb, load_families
from dss.engine import rank_families


def main():
    st.title("ML Algorithm Selection DSS")
    st.caption("Domain + Data Modality + Constraints → Algorithm Families + Examples (rule-based, explainable)")

    kb = load_kb("data/knowledge_base.yaml")
    domains = kb.get("domains", {})
    modalities = kb.get("modalities", {})


    domain_key = st.selectbox(
        "Domain",
        list(domains.keys()),
        format_func=lambda k: f"{domains[k]} ({k})"
    )

    modality_key = st.selectbox(
        "Data modality",
        list(modalities.keys()),
        format_func=lambda k: f"{modalities[k]} ({k})"
    )

    goal = st.radio(
        "Primary goal",
        ["classification", "regression", "clustering", "anomaly_detection"],
        horizontal=True
    )

    st.divider()
    st.subheader("Constraints / Practical needs")

    col1, col2 = st.columns(2)
    with col1:
        interpretability = st.checkbox("Interpretability required (must be explainable)?", value=False)
        limited_labels = st.checkbox("Limited labeled data?", value=False)
    with col2:
        privacy_sensitive = st.checkbox("Privacy-sensitive / regulated data?", value=False)
        real_time = st.checkbox("Real-time / low-latency required?", value=False)

    needs = UserNeeds(
        domain=domain_key,
        modality=modality_key,
        goal=goal,
        interpretability=interpretability,
        privacy_sensitive=privacy_sensitive,
        limited_labels=limited_labels,
        real_time=real_time
    )

    st.divider()


    if "ranked" not in st.session_state:
        st.session_state.ranked = []

    if st.button("Get Recommendations", type="primary"):
        families = load_families("data/knowledge_base.yaml")
        st.session_state.ranked = rank_families(needs, families)

        if not st.session_state.ranked:
            st.warning("No strong matches found. Try relaxing constraints or changing domain/modality.")

    ranked = st.session_state.ranked

    if ranked:
        st.subheader("Top Recommendations (Algorithm Families)")

        for i, (family, score, reasons, examples) in enumerate(ranked[:3], start=1):
            with st.expander(f"{i}) {family}  (score: {score})", expanded=(i == 1)):
                st.markdown("**Example models:**")
                st.write(", ".join(examples))

                st.markdown("**Why this was recommended:**")
                for r in reasons[:8]:
                    st.write(f"- {r}")

        st.info("Engine is rule-based for consistency and explainability. The knowledge base is editable in YAML.")


        report_text = "ML Algorithm Selection Report\n"
        report_text += "=" * 40 + "\n\n"
        report_text += f"Domain: {domain_key}\n"
        report_text += f"Data Modality: {modality_key}\n"
        report_text += f"Primary Goal: {goal}\n\n"

        report_text += "Constraints:\n"
        report_text += f"- Interpretability: {interpretability}\n"
        report_text += f"- Privacy Sensitive: {privacy_sensitive}\n"
        report_text += f"- Limited Labels: {limited_labels}\n"
        report_text += f"- Real-time Required: {real_time}\n\n"

        report_text += "Top Recommendations:\n\n"

        for i, (family, score, reasons, examples) in enumerate(ranked[:3], start=1):
            report_text += f"{i}) {family} (Score: {score})\n"
            report_text += f"   Examples: {', '.join(examples)}\n"
            report_text += "   Reasons:\n"
            for r in reasons[:5]:
                report_text += f"     - {r}\n"
            report_text += "\n"

        st.download_button(
            label="Download Decision Report",
            data=report_text,
            file_name="ml_dss_decision_report.txt",
            mime="text/plain"
        )


if __name__ == "__main__":
    main()
