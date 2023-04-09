from pathlib import Path


def get_code_example(filename):
    # Render the readme as markdown using st.markdown.
    txt = Path(f"docs/code_examples/{filename}.md").read_text()
    # st.markdown(txt)
    return txt
