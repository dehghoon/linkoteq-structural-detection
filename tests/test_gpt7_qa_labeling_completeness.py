from pathlib import Path

CONTRACT = Path("contracts/gpt7-qa-labeling-completeness-v0.1.md")

def test_gpt7_qa_completeness_contract_is_present_and_mandatory():
    text = CONTRACT.read_text(encoding="utf-8")
    required = [
        "MUST read and apply both this contract",
        "MUST NOT cherry-pick only the clearest subset",
        "at least one visible end meets an identifiable column",
        "NO-SAFE-BOX",
        "MUST NOT be treated as background or negative training evidence",
        "Mandatory completeness pass",
        "source-page",
        "Only explicit human QA",
        "MUST NOT be interpreted as approval of unseen boxes",
    ]
    for phrase in required:
        assert phrase in text, f"missing mandatory GPT-7 QA invariant: {phrase}"

def test_contract_preserves_gpt6_boundary_and_wall_ambiguity_rule():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "No `ambiguous-wall` class is permitted." in text
    assert "MUST NOT encode engineering centerlines, endpoints, connectivity, topology" in text
