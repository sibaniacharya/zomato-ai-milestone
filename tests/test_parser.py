import pytest
import json
from src.services.parser import ResponseParser, ParseError

@pytest.fixture
def parser():
    return ResponseParser()

@pytest.fixture
def candidate_ids():
    return {"1", "2", "3"}

def test_parse_valid_json(parser, candidate_ids):
    raw = json.dumps({
        "summary": "Good choices.",
        "recommendations": [
            {"id": "1", "rank": 1, "explanation": "Top choice."},
            {"id": "2", "rank": 2, "explanation": "Second choice."}
        ]
    })
    res = parser.parse(raw, candidate_ids)
    assert res["summary"] == "Good choices."
    assert len(res["recommendations"]) == 2
    assert res["recommendations"][0]["id"] == "1"

def test_parse_missing_summary(parser, candidate_ids):
    raw = json.dumps({
        "recommendations": [{"id": "1", "rank": 1, "explanation": "Top choice."}]
    })
    with pytest.raises(ParseError) as exc:
        parser.parse(raw, candidate_ids)
    assert "summary" in str(exc.value).lower()

def test_parse_missing_recommendations(parser, candidate_ids):
    raw = json.dumps({
        "summary": "Good choices."
    })
    with pytest.raises(ParseError) as exc:
        parser.parse(raw, candidate_ids)
    assert "recommendations" in str(exc.value).lower()

def test_parse_invalid_id(parser, candidate_ids):
    raw = json.dumps({
        "summary": "Good choices.",
        "recommendations": [
            {"id": "99", "rank": 1, "explanation": "Top choice."}
        ]
    })
    with pytest.raises(ParseError) as exc:
        parser.parse(raw, candidate_ids)
    assert "Hallucinated ID" in str(exc.value)

def test_parse_malformed_json(parser, candidate_ids):
    raw = "Here are my recommendations: { summary: "
    with pytest.raises(ParseError) as exc:
        parser.parse(raw, candidate_ids)
    assert "Invalid JSON" in str(exc.value)
