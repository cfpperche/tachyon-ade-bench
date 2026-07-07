DEFAULT_FLAGS = {
    "beta_checkout": False,
    "legacy_export": True,
}


def is_enabled(name, overrides=None):
    if overrides and name in overrides:
        return bool(overrides[name])
    return bool(DEFAULT_FLAGS.get(name, False))


def enabled_flags(overrides=None):
    return [
        name
        for name, enabled in DEFAULT_FLAGS.items()
        if is_enabled(name, overrides)
    ]

