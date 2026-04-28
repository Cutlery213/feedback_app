from app import FeedbackParser

def test_parser():
    parser = FeedbackParser()
    
    # Test case 1: Standard
    text1 = "Alice: 1) Typo at 0:45 2) More diagrams 3) Very clear!"
    res1 = parser.parse_cell(text1)
    assert res1["name"] == "Alice"
    assert res1["q1"] == "Typo at 0:45"
    assert res1["q2"] == "More diagrams"
    assert res1["q3"] == "Very clear!"
    
    # Test case 2: Multi-line
    text2 = """Bob: 1) The first part
    has multiple lines. 2) Summary 
    slide needed. 3) Good intro"""
    res2 = parser.parse_cell(text2)
    assert res2["name"] == "Bob"
    assert "multiple lines" in res2["q1"]
    assert "Summary" in res2["q2"]
    
    # Test case 3: Varied spacing and markers
    text3 = " Charlie : 1)Missing code 2)  Practice 3)End "
    res3 = parser.parse_cell(text3)
    assert res3["name"] == "Charlie"
    assert res3["q1"] == "Missing code"
    assert res3["q2"] == "Practice"
    assert res3["q3"] == "End"
    
    print("All parser tests passed!")

if __name__ == "__main__":
    test_parser()
