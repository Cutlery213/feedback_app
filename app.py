import pandas as pd
import re
import io
import streamlit as st

class FeedbackParser:
    def __init__(self):
        # Flexible regex to match 1. or 1) etc.
        self.q1_pattern = re.compile(r"[1]\s*[\.\)]\s*(.*?)\s*(?=[2]\s*[\.\)]|$)", re.DOTALL | re.IGNORECASE)
        self.q2_pattern = re.compile(r"[2]\s*[\.\)]\s*(.*?)\s*(?=[3]\s*[\.\)]|$)", re.DOTALL | re.IGNORECASE)
        self.q3_pattern = re.compile(r"[3]\s*[\.\)]\s*(.*)$", re.DOTALL | re.IGNORECASE)

    def parse_cell(self, text):
        if not isinstance(text, str) or not text.strip():
            return None
        
        text = text.strip()
        if text.upper() == "N/A" or text.upper() == "NA":
            return None

        q1 = self.q1_pattern.search(text)
        q2 = self.q2_pattern.search(text)
        q3 = self.q3_pattern.search(text)

        if q1 or q2 or q3:
            return {
                "q1": q1.group(1).strip() if q1 else "",
                "q2": q2.group(1).strip() if q2 else "",
                "q3": q3.group(1).strip() if q3 else ""
            }
        
        # If no markers found but there is text, treat it as Q1 or general feedback
        return {
            "q1": text,
            "q2": "",
            "q3": ""
        }

def process_dataframe(df, module_name):
    parser = FeedbackParser()
    all_records = []

    # Find the header row that contains "Video"
    video_row_idx = -1
    for i in range(min(5, len(df))):
        row_values = [str(x) if x is not None else "" for x in df.iloc[i]]
        if any("Video" in val for val in row_values):
            video_row_idx = i
            break
    
    if video_row_idx == -1:
        # Fallback: maybe first row is header?
        video_row_idx = 0

    video_row = df.iloc[video_row_idx]
    video_cols = []
    for i, col_val in enumerate(video_row):
        if isinstance(col_val, str) and "Video" in col_val:
            video_cols.append(i)
    
    # Data starts after the video header row
    # Skip one more row if it looks like an example row (contains "eg:")
    start_row = video_row_idx + 1
    if start_row < len(df):
        example_row_values = [str(x) if x is not None else "" for x in df.iloc[start_row]]
        if any("eg:" in val.lower() or "eg " in val.lower() for val in example_row_values):
            start_row += 1

    for row_idx in range(start_row, len(df)):
        row = df.iloc[row_idx]
        psa_name = row[0]
        if pd.isna(psa_name) or str(psa_name).strip() == "" or "eg PSA" in str(psa_name):
            continue
            
        for col_idx in video_cols:
            if col_idx >= len(row):
                continue
            video_name = str(video_row[col_idx]).strip()
            cell_content = row[col_idx]
            
            parsed = parser.parse_cell(cell_content)
            if parsed:
                parsed["name"] = str(psa_name).strip()
                parsed["video"] = video_name
                parsed["module"] = module_name
                all_records.append(parsed)
    
    return all_records

def load_file(uploaded_file):
    all_records = []
    file_name = uploaded_file.name
    
    if file_name.endswith('.csv'):
        # Try different encodings for CSV
        try:
            df = pd.read_csv(uploaded_file, header=None)
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, header=None, encoding='latin1')
        
        # For CSV, we treat filename as module name
        module_name = re.sub(r'\.csv$', '', file_name, flags=re.I)
        all_records.extend(process_dataframe(df, module_name))
    
    elif file_name.endswith(('.xlsx', '.xls')):
        excel_file = pd.ExcelFile(uploaded_file)
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
            all_records.extend(process_dataframe(df, sheet_name))
            
    return all_records

if __name__ == "__main__":
    st.set_page_config(page_title="Feedback Compiler", layout="wide")
    st.title("📑 Qualitative Feedback Compiler")
    st.write("Extract and organize qualitative feedback from your module trackers.")

    uploaded_file = st.file_uploader("Choose a feedback file (Excel or CSV)", type=["xlsx", "xls", "csv"])

    if uploaded_file:
        try:
            records = load_file(uploaded_file)
            if records:
                st.success(f"Successfully parsed {len(records)} feedback entries!")
                st.session_state['records'] = records
            else:
                st.warning("No feedback entries found. Please check the file format.")
        except Exception as e:
            st.error(f"Error processing file: {e}")
            import traceback
            st.code(traceback.format_exc())

    if 'records' in st.session_state:
        records = st.session_state['records']
        view_mode = st.radio("Select View Mode", ["Compiled View", "Thematic View"])
        
        if view_mode == "Compiled View":
            st.header("Module & Video Feedback")
            
            modules = sorted(list(set(r['module'] for r in records)))
            selected_module = st.selectbox("Select Module", modules)
            
            module_records = [r for r in records if r['module'] == selected_module]
            videos = sorted(list(set(r['video'] for r in module_records)))
            
            for video in videos:
                with st.expander(f"🎬 {video}", expanded=True):
                    video_records = [r for r in module_records if r['video'] == video]
                    for r in video_records:
                        st.subheader(f"👤 {r['name']}")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.info("**Q1: Incorrect/Needs Update?**")
                            st.write(r['q1'] if r['q1'] else "_No feedback_")
                        with col2:
                            st.info("**Q2: Missing/Want More?**")
                            st.write(r['q2'] if r['q2'] else "_No feedback_")
                        with col3:
                            st.info("**Q3: Other Feedback?**")
                            st.write(r['q3'] if r['q3'] else "_No feedback_")
                        st.divider()
        else:
            st.header("Thematic Question Analysis")
            question_choice = st.selectbox(
                "Select Question to Analyze",
                [
                    "Q1: Is anything incorrect or needs updating?",
                    "Q2: Is anything missing, or is there something you’d like more of?",
                    "Q3: Any other feedback or suggestions?"
                ]
            )
            
            q_key = "q1" if "Q1" in question_choice else "q2" if "Q2" in question_choice else "q3"
            
            for r in records:
                if r[q_key].strip():
                    with st.container():
                        st.markdown(f"**{r['name']}** ({r['module']} > {r['video']})")
                        st.write(r[q_key])
                        st.divider()
