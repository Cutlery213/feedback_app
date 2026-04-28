import pandas as pd

def create_mock_excel():
    # Module 1 data
    data_m1 = {
        "Intro Video": [
            "Alice: 1) Typo at 0:45 2) More diagrams 3) Very clear!",
            "Bob: 1) None 2) Summary slide 3) Good intro"
        ],
        "Technical Video": [
            "Charlie: 1) Code snippet missing 2) Practice files 3) Challenging",
            "Alice: 1) Versioning updated? 2) Link to docs 3) Helpful"
        ]
    }
    df1 = pd.DataFrame(data_m1)

    # Module 2 data
    data_m2 = {
        "Advanced Video": [
            "Dave: 1) Audio glitch at 2:00 2) Q&A session 3) Impressed",
            "Eve: 1) Incorrect link in description 2) Case studies 3) Excellent"
        ]
    }
    df2 = pd.DataFrame(data_m2)

    with pd.ExcelWriter("mock_feedback.xlsx") as writer:
        df1.to_excel(writer, sheet_name="Module 1", index=False)
        df2.to_excel(writer, sheet_name="Module 2", index=False)

if __name__ == "__main__":
    create_mock_excel()
    print("Created mock_feedback.xlsx")
