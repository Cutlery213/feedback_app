from app import load_file
import os
import io

def test_e2e():
    mock_file_path = "mock_feedback.xlsx"
    if not os.path.exists(mock_file_path):
        print("Mock file not found. Run generate_mock_excel.py first.")
        return
    
    # We need to simulate the streamlit uploaded file object
    with open(mock_file_path, "rb") as f:
        class FileObj(io.BytesIO):
            def __init__(self, content, name):
                super().__init__(content)
                self.name = name
        
        file_obj = FileObj(f.read(), mock_file_path)
        records = load_file(file_obj)
    
    # We expect 5 entries from the mock generator
    assert len(records) == 5
    
    # Check Module 1, Video 1 (Intro Video)
    alice_m1 = [r for r in records if r["name"] == "Alice" and r["module"] == "Module 1" and r["video"] == "Intro Video"]
    assert len(alice_m1) == 1
    assert alice_m1[0]["q1"] == "Typo at 0:45"
    
    # Check Module 2
    dave_m2 = [r for r in records if r["name"] == "Dave" and r["module"] == "Module 2"]
    assert len(dave_m2) == 1
    assert "Audio glitch" in dave_m2[0]["q1"]
    
    print(f"End-to-End test passed! Successfully processed {len(records)} records.")

if __name__ == "__main__":
    test_e2e()
