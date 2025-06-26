
import re
import json
from config import KEY_PATTERNS, CONTEXT_KEYWORDS, HIGH_ENTROPY_REGEX, ENTROPY_THRESHOLDS, MNEMO
from entropy import shannon_entropy
from utils import get_context_snippet, in_context, iter_json_strings

def scan_text(text: str):
    findings = []
    for name, pattern in KEY_PATTERNS.items():
        for m in pattern.finditer(text):
            val = m.group(0).strip()
            ctx = get_context_snippet(text, m.start(), m.end())
            if name == 'BIP39 Seed Phrase':
                words = val.split()
                if len(words) in (12, 24) and MNEMO.check(val) and in_context(text, m.start(), m.end()):
                    findings.append((name, val, ctx))
            else:
                findings.append((name, val, ctx))

    for m in HIGH_ENTROPY_REGEX.finditer(text):
        val = m.group(0)
        ent = shannon_entropy(val)
        kind = None
        if re.fullmatch(r'[A-Za-z0-9+/=]+', val) and ent >= ENTROPY_THRESHOLDS['base64']:
            kind = 'High Entropy (Base64)'
        elif re.fullmatch(r'[0-9a-fA-F]+', val) and ent >= ENTROPY_THRESHOLDS['hex']:
            kind = 'High Entropy (Hex)'
        if kind and in_context(text, m.start(), m.end()):
            ctx = get_context_snippet(text, m.start(), m.end())
            findings.append((kind, val, ctx))

    try:
        obj = json.loads(text)
        for s in iter_json_strings(obj):
            for name, val, ctx in scan_text(s):
                findings.append((name + " (in JSON)", val, ctx))
    except json.JSONDecodeError:
        pass

    return findings
