import pandas as pd

def create_mock_excel():
    # New format:
    # Row 0: PSA Name, Feedback Guide ..., ...
    # Row 1: , Video 1, Video 2, ...
    # Row 2: eg PSA, eg:, eg:, ...
    # Row 3: Name1, Feedback1, Feedback2, ...

    # Module 1 data
    data_m1 = [
        ["PSA Name", "Feedback Guide", None, None],
        [None, "Intro Video", "Technical Video", None],
        ["eg PSA", "eg: 1) ...", "eg: 1) ...", None],
        ["Alice", "1) Typo at 0:45 2) More diagrams 3) Very clear!", "1) Versioning updated? 2) Link to docs 3) Helpful"],
        ["Bob", "1) None 2) Summary slide 3) Good intro", "N/A"]
    ]
    df1 = pd.DataFrame(data_m1)

    # Module 2 data
    data_m2 = [
        ["PSA Name", "Feedback Guide", None],
        [None, "Advanced Video", None],
        ["eg PSA", "eg: 1) ...", None],
        ["Dave", "1. Audio glitch at 2:00 2. Q&A session 3. Impressed"],
        ["Eve", "1. Incorrect link in description 2. Case studies 3. Excellent"]
    ]
    df2 = pd.DataFrame(data_m2)

    with pd.ExcelWriter("mock_feedback.xlsx") as writer:
        df1.to_excel(writer, sheet_name="Module 1", index=False, header=False)
        df2.to_excel(writer, sheet_name="Module 2", index=False, header=False)

if __name__ == "__main__":
    create_mock_excel()
    print("Created mock_feedback.xlsx in the new format")
