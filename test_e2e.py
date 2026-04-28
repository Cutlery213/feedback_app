from app import process_feedback_file
import os

def test_e2e():
    mock_file = "mock_feedback.xlsx"
    if not os.path.exists(mock_file):
        print("Mock file not found. Run generate_mock_excel.py first.")
        return
    
    records = process_feedback_file(mock_file)
    
    # We expect 6 entries from the mock generator
    # Module 1: 2 videos * 2 responses = 4
    # Module 2: 1 video * 2 responses = 2
    # Total = 6
    assert len(records) == 6
    
    # Check Module 1, Video 1
    alice_m1 = [r for r in records if r["name"] == "Alice" and r["module"] == "Module 1" and r["video"] == "Intro Video"]
    assert len(alice_m1) == 1
    assert alice_m1[0]["q1"] == "Typo at 0:45"
    
    print(f"End-to-End test passed! Successfully processed {len(records)} records.")

if __name__ == "__main__":
    test_e2e()
