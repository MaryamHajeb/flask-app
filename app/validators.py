"""Request validation helpers."""

import re

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
FIELDS = {"name": 100, "email": 120, "department": 100}


def validate_student_payload(payload, *, partial=False):
    """Return (cleaned_data, errors) for a create or update request."""
    if not isinstance(payload, dict):
        return {}, {"body": "A JSON object is required."}

    errors = {}
    cleaned = {}
    for field, max_length in FIELDS.items():
        if field not in payload:
            if not partial:
                errors[field] = "This field is required."
            continue

        value = payload[field]
        if not isinstance(value, str) or not value.strip():
            errors[field] = "Must be a non-empty string."
            continue

        value = value.strip()
        if len(value) > max_length:
            errors[field] = f"Must be at most {max_length} characters."
            continue
        if field == "email" and not EMAIL_PATTERN.fullmatch(value):
            errors[field] = "Must be a valid email address."
            continue
        cleaned[field] = value

    extra_fields = set(payload) - set(FIELDS)
    if extra_fields:
        errors["fields"] = f"Unsupported fields: {', '.join(sorted(extra_fields))}."
    return cleaned, errors
