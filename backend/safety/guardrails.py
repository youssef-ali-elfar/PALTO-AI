import re


def validate_answer(answer, evidence_found, intent="CLINICAL"):
    """
    Validate and clean PALTO's answer.

    Important:
    - Never add an "insufficient evidence" prefix.
    - General questions should pass normally.
    - Clinical answers are only cleaned for unsafe certainty language.
    """

    if not answer:
        return answer

    # Safety language cleanup
    for pattern in [
        r"\bguaranteed\b",
        r"\b100% safe\b",
        r"\bdefinitely safe\b",
    ]:
        answer = re.sub(
            pattern,
            "not established from the available evidence",
            answer,
            flags=re.I,
        )

    return answer