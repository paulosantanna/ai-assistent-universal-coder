"""Lookup over the local audio-engineering corpus."""
from corpus import SOURCES, TOPICS
from measure import erb, eyring_rt60, hz_from_cents, hz_from_note, nyquist, sabine_rt60, wavelength

SOURCE_BY_ID = {item["id"]: item for item in SOURCES}
TOPIC_BY_ID = {item["id"]: item for item in TOPICS}


def health():
    orgs = sorted({item["org"] for item in SOURCES})
    return {
        "name": "audio-engineering",
        "version": "1.0.0",
        "protocol": "jsonrpc-stdio",
        "topics": len(TOPICS),
        "sources": len(SOURCES),
        "organizations": orgs,
        "engine": "parametric-formant",
        "ceiling": "parametric-formant; no donor audio; no commercial voice API",
        "secret_policy": "runtime-references-only",
    }


def search(query, limit=8):
    terms = [part for part in str(query).lower().split() if len(part) > 1]
    if not terms:
        raise ValueError("query is empty")
    limit = max(1, min(int(limit), 20))
    ranked = []
    for topic in TOPICS:
        haystack = " ".join([
            topic["id"], topic["title"], topic["domain"], topic["summary"],
            " ".join(topic["points"]), " ".join(topic["source_ids"]),
        ]).lower()
        score = sum(haystack.count(term) for term in terms)
        if score:
            ranked.append((score, topic))
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [
        {"id": topic["id"], "title": topic["title"], "domain": topic["domain"], "score": score}
        for score, topic in ranked[:limit]
    ]


def topic(topic_id):
    found = TOPIC_BY_ID.get(topic_id)
    if found is None:
        raise KeyError(topic_id)
    payload = dict(found)
    payload["sources"] = [SOURCE_BY_ID[source_id] for source_id in found["source_ids"]]
    return payload


def sources(org=None):
    rows = SOURCES
    if org:
        needle = org.lower()
        rows = [item for item in SOURCES if needle in item["org"].lower() or needle in item["id"]]
    return {"count": len(rows), "sources": rows}


def calculate(operation, arguments):
    arguments = arguments or {}
    if operation == "nyquist":
        value = nyquist(arguments["sample_rate"])
        formula = "nyquist_hz = sample_rate / 2"
    elif operation == "wavelength":
        value = wavelength(arguments["frequency_hz"], arguments.get("speed_m_s", 343.0))
        formula = "wavelength_m = speed_m_s / frequency_hz"
    elif operation == "sabine":
        value = sabine_rt60(arguments["volume_m3"], arguments["absorption_sabins"])
        formula = "RT60 = 0.161 * volume_m3 / absorption_sabins"
    elif operation == "eyring":
        value = eyring_rt60(arguments["volume_m3"], arguments["surface_m2"], arguments["alpha"])
        formula = "RT60 = 0.161 * volume_m3 / (-surface_m2 * ln(1 - alpha))"
    elif operation == "erb":
        value = erb(arguments["frequency_hz"])
        formula = "ERB = 24.7 * (4.37 * frequency_khz + 1)"
    elif operation == "cents":
        value = hz_from_cents(arguments["reference_hz"], arguments["cents"])
        formula = "hz = reference_hz * 2 ** (cents / 1200)"
    elif operation == "note":
        value = hz_from_note(arguments["note"])
        formula = "A4 = 440 Hz"
    else:
        raise ValueError("unknown operation")
    return {
        "operation": operation,
        "value": value,
        "formula": formula,
        "note": "Named formula for engineering use. Standards bodies' texts are not reproduced.",
    }
