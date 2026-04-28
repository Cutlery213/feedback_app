from app import FeedbackParser

def test_parser():
    parser = FeedbackParser()
    
    # Test case 1: Standard new format with dots
    text1 = "1. Typo at 0:45 2. More diagrams 3. Very clear!"
    res1 = parser.parse_cell(text1)
    assert res1["q1"] == "Typo at 0:45"
    assert res1["q2"] == "More diagrams"
    assert res1["q3"] == "Very clear!"
    
    # Test case 2: Parentheses
    text2 = "1) The first part 2) Summary 3) Good intro"
    res2 = parser.parse_cell(text2)
    assert res2["q1"] == "The first part"
    assert res2["q2"] == "Summary"
    assert res2["q3"] == "Good intro"
    
    # Test case 3: Multi-line and missing parts
    text3 = """1. First part
    with lines
    3. Final part"""
    res3 = parser.parse_cell(text3)
    assert "with lines" in res3["q1"]
    assert res3["q2"] == ""
    assert res3["q3"] == "Final part"

    # Test case 4: No markers
    text4 = "Just some general feedback here."
    res4 = parser.parse_cell(text4)
    assert res4["q1"] == "Just some general feedback here."
    assert res4["q2"] == ""
    assert res4["q3"] == ""
    
    print("All parser tests passed!")

if __name__ == "__main__":
    test_parser()
