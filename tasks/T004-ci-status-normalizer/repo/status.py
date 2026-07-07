VALID_STATUSES = {
    "todo",
    "in_progress",
    "blocked",
    "done",
}


def normalize_status(raw):
    if raw is None:
        return "unknown"
    value = raw.strip().lower().replace(" ", "_")
    if value in VALID_STATUSES:
        return value
    return "unknown"

