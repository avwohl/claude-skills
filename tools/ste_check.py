#!/usr/bin/env python3
"""
ste_check.py -- mechanical ASD-STE100 checks for Markdown documentation.

Implements the mechanically-checkable subset of the rules described in
skills/simplified-technical-english.md (Part 10).  It does NOT check the rules
that need judgment (approved meaning, technical-noun categorization, one topic
per paragraph, whether a rewrite kept the meaning).

It ships no dictionary.  ASD-STE100 Part 2 is copyright ASD, Brussels, and may
not be redistributed here.  Get the free official copy from https://asd-ste100.org/

Tier E regions (code fences, inline code, URLs, badges, front matter, HTML,
ASCII art, tables) are skipped, per the skill's skip-region list.

Usage:
    python3 tools/ste_check.py README.md
    python3 tools/ste_check.py --tier A docs/INSTALL.md
    python3 tools/ste_check.py --json before.md after.md
    python3 tools/ste_check.py --quiet --max-issues 0 README.md   # CI gate
"""

import argparse
import json
import re
import sys

# ---------------------------------------------------------------- constants

TIER_LIMITS = {"A": 20, "B": 25, "C": None, "D": None, "E": None}

CONTRACTIONS = re.compile(
    r"\b(\w+)'(s|t|re|ve|ll|d|m)\b(?!\s*\))", re.IGNORECASE)

LATIN = re.compile(r"\b(e\.g\.|i\.e\.|etc\.|vs\.|via|N/A|cf\.|et al\.)", re.IGNORECASE)

BE_FORMS = r"(?:is|are|was|were|be|been|being|get|gets|got)"
PASSIVE = re.compile(
    r"\b" + BE_FORMS + r"\s+(?:\w+ly\s+)?(\w+(?:ed|en|own| built|made|done|set|put|read|kept))\b",
    re.IGNORECASE)

# -ing words that are legitimate technical nouns / established compounds.
ING_ALLOW = {
    "operating", "floating", "programming", "string", "thing", "during",
    "engineering", "debugging", "encoding", "logging", "listing", "mapping",
    "padding", "casting", "rounding", "scaling", "timing", "polling",
    "banking", "caching", "chaining", "indexing", "parsing", "linking",
    "swapping", "paging", "streaming", "buffering", "handling", "processing",
    "computing", "networking", "settings", "warning", "meaning", "bring",
    "king", "ring", "wing", "sing", "spring", "according", "including",
    "remaining", "following", "existing", "missing", "leading", "trailing",
    "underlying", "corresponding", "resulting", "incoming", "outgoing",
    "working", "running",  # flagged only in headings
    # -ing modifiers inside established technical nouns (rule 3.5 permits these)
    "signing", "rendering", "merging", "switching", "shipping", "packaging",
    "addressing", "branching", "pipelining", "profiling", "tracing", "linking",
}

BANNED = {
    "leverage": "use", "leverages": "uses", "leveraging": "using",
    "utilize": "use", "utilizes": "uses", "utilizing": "using",
    "facilitate": "lets you", "facilitates": "lets you",
    "robust": "state the property", "seamless": "delete",
    "seamlessly": "delete", "powerful": "delete", "blazing": "give the number",
    "simply": "delete", "just": "delete", "easily": "delete",
    "merely": "delete", "effortlessly": "delete",
    "comprehensive": "list what it does", "full-featured": "list what it does",
    "cutting-edge": "delete", "state-of-the-art": "delete",
    "perform": "do, or the real verb", "performs": "does, or the real verb",
    "carry out": "do", "prior to": "before", "subsequent to": "after",
    "in order to": "to", "in the event that": "if", "a number of": "the number",
    "ensure": "make sure that", "ensures": "makes sure that",
    "desired": "the one you want", "appropriate": "the correct",
    "please": "delete", "feel free": "you can",
    "out of the box": "with no configuration", "under the hood": "internally",
    "kick off": "start", "tweak": "adjust", "nuke": "delete",
    "blow away": "delete", "clobber": "overwrite", "brick": "make unserviceable",
    "gotcha": "a known problem", "sanity check": "a check for correctness",
    "sane": "correct", "dummy": "placeholder", "whitelist": "allowlist",
    "blacklist": "denylist", "master": "primary", "slave": "replica",
    "shall": "must", "and/or": "and, or, or name both cases",
    "choke": "stop with an error", "chokes": "stops with an error",
    "barf": "stop with an error", "handy": "useful", "nifty": "useful",
}

PHRASAL = {
    "set up": "prepare", "carry out": "do", "back up": "make a backup of",
    "turn on": "start", "turn off": "stop", "shut down": "stop",
    "figure out": "determine", "find out": "determine", "come up with": "make",
}

# ------------------------------------------------------------- segmentation


def segment(text):
    """Split markdown into (kind, lineno, content) where kind is prose|skip.

    Prose is what STE applies to.  Everything else is Tier E.
    """
    lines = text.split("\n")
    out = []
    in_fence = False
    fence_tok = None
    in_front = False

    for i, raw in enumerate(lines, 1):
        line = raw.rstrip("\n")
        stripped = line.strip()

        # YAML front matter
        if i == 1 and stripped == "---":
            in_front = True
            out.append(("skip", i, line))
            continue
        if in_front:
            out.append(("skip", i, line))
            if stripped == "---":
                in_front = False
            continue

        # fenced code
        m = re.match(r"^(\s*)(`{3,}|~{3,})", line)
        if m and not in_fence:
            in_fence, fence_tok = True, m.group(2)[0]
            out.append(("skip", i, line))
            continue
        if in_fence:
            out.append(("skip", i, line))
            if re.match(r"^\s*" + re.escape(fence_tok) + r"{3,}\s*$", line):
                in_fence = False
            continue

        # tables, ascii art, html, badges, indented code, blank
        if (stripped.startswith("|")
                or stripped.startswith("<")
                or re.match(r"^\s*[├└│─┌┐┘┴┬┼]", line)
                or re.match(r"^\s*\[!\[", stripped)
                or re.match(r"^\s{4,}\S", line) and not re.match(r"^\s*[-*+\d]", stripped)
                or not stripped):
            out.append(("skip", i, line))
            continue

        out.append(("prose", i, line))
    return out


def strip_inline(s):
    """Replace Tier E inline spans with a single-token placeholder (counts as 1)."""
    s = re.sub(r"`[^`]*`", " CODETOKEN ", s)
    s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r" \1 ", s)      # links: keep label
    s = re.sub(r"https?://\S+", " URLTOKEN ", s)
    s = re.sub(r"\*\*([^*]*)\*\*", r"\1", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", s)
    s = re.sub(r"[$][A-Z_]+", " VARTOKEN ", s)
    return s


def sentences(par):
    """Split a paragraph into sentences, protecting common abbreviations."""
    p = re.sub(r"\b([A-Z])\.", r"\1<DOT>", par)
    p = re.sub(r"\b(v|no|vol|fig|approx|Mr|Mrs|Dr|St|e\.g|i\.e|etc)\.",
               r"\1<DOT>", p, flags=re.IGNORECASE)
    p = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", p)
    parts = re.split(r"(?<=[.!?:])\s+", p)
    return [x.replace("<DOT>", ".").strip() for x in parts if x.strip()]


def ste_word_count(sentence):
    """Count words the way rules 8.4-8.7 count them (plus the skill's software
    extension: an inline code span, path, URL, flag, or identifier is one word)."""
    s = sentence
    s = re.sub(r"\([^)]*\)", " PARENTOKEN ", s)          # 8.5 parenthetical = 1
    s = re.sub(r'"[^"]*"', " QUOTETOKEN ", s)            # 8.6 quoted text = 1
    s = re.sub(r"\b\d[\d,._]*\s*(?:[A-Za-z]{1,4}\b)?", " NUMTOKEN ", s)  # 8.6 number(+unit)
    s = re.sub(r"\b[A-Za-z]+[\d?]+[A-Za-z\d?]*\b", " IDTOKEN ", s)       # alphanumeric id
    s = re.sub(r"\S*/\S*", " PATHTOKEN ", s)             # path
    tokens = [t for t in re.split(r"[\s]+", s) if t.strip(".,:;!?—-")]
    return len(tokens)


# ------------------------------------------------------------------ checks


def check(path, tier="B", explicit_limit=None):
    text = open(path, encoding="utf-8").read()
    seg = segment(text)
    issues = []

    def add(rule, lineno, msg, snippet=""):
        issues.append({"rule": rule, "line": lineno, "message": msg,
                       "snippet": snippet[:110]})

    # Group prose into paragraphs.  A heading or a list bullet always starts a
    # new unit: rules 6.3/6.6 apply per list item, not to the list as a whole,
    # and merging a bullet list into one block produces nonsense word counts.
    bullet = re.compile(r"^\s*([-*+]|\d+[.)])\s")
    paragraphs, cur = [], []
    for kind, ln, line in seg:
        if kind != "prose":
            if cur:
                paragraphs.append(cur)
                cur = []
            continue
        starts_unit = bullet.match(line) or line.lstrip().startswith("#")
        if starts_unit and cur:
            paragraphs.append(cur)
            cur = []
        cur.append((ln, line))
    if cur:
        paragraphs.append(cur)

    limit = explicit_limit if explicit_limit else TIER_LIMITS.get(tier)

    # Tier gating, per Part 2 of the skill.  Tier E is frozen: nothing applies,
    # and its invariant (byte-identical) is checked by diffing, not by linting.
    # Tier D is VOICE: only terminology consistency and inclusive language, so
    # that a rewrite cannot delete a hedge and turn a calibrated claim into an
    # overclaim.  Tier C is fragments by design: no sentence or article rules.
    if tier == "E":
        return []
    voice_only = (tier == "D")
    fragments = (tier == "C")

    for par in paragraphs:
        first_ln = par[0][0]
        is_heading = par[0][1].lstrip().startswith("#")
        is_list = bool(bullet.match(par[0][1]))
        body = " ".join(l for _, l in par)
        if is_list:
            body = bullet.sub("", par[0][1]) + " " + " ".join(l for _, l in par[1:])
        clean = strip_inline(body)
        clean_nohash = re.sub(r"^#+\s*", "", clean).strip()

        sents = sentences(clean_nohash)

        # 6.6 paragraph length
        if not (voice_only or fragments) and not is_heading and not is_list and len(sents) > 6:
            add("6.6", first_ln,
                f"paragraph has {len(sents)} sentences (max 6)")

        for sent in sents:
            n = ste_word_count(sent)
            raw = len([t for t in sent.split() if t.strip(".,:;!?—-")])
            if limit and not is_heading:
                if n > limit:
                    add("5.1" if tier == "A" else "6.3", first_ln,
                        f"sentence is {n} STE words / {raw} raw (max {limit})", sent)
                elif raw > int(limit * 1.6):
                    # Abuse guard the standard does not have: a 60-token shell
                    # pipeline inside one code span counts as 1 STE word and
                    # would otherwise smuggle an unreadable line past the limit.
                    add("5.1!" if tier == "A" else "6.3!", first_ln,
                        f"sentence passes STE count ({n}) but is {raw} raw "
                        f"tokens — too dense to read", sent)

            if voice_only:
                # Tier D: glossary terms and inclusive language only.  Deliberate
                # no-op for length, voice, tense, punctuation and filler.
                low = " " + sent.lower() + " "
                for bad in ("whitelist", "blacklist", "master", "slave",
                            "sane", "sanity check", "dummy"):
                    if re.search(r"(?<![\w-])" + re.escape(bad) + r"(?![\w-])", low):
                        add("GR-7", first_ln,
                            f"non-inclusive term '{bad}' (permitted edit at Tier D)", sent)
                continue

            # 8.1 semicolon
            if ";" in sent:
                add("8.1", first_ln, "semicolon is not permitted", sent)

            # 4.2 contractions (sentence rule: off for Tier C fragments)
            for m in (() if fragments else CONTRACTIONS.finditer(sent)):
                if m.group(2).lower() == "s" and m.group(1)[0].isupper():
                    continue          # likely a possessive proper noun
                add("4.2", first_ln, f"contraction '{m.group(0)}'", sent)

            # GR-6 Latin abbreviations
            for m in LATIN.finditer(sent):
                add("GR-6", first_ln,
                    f"Latin abbreviation or 'via': '{m.group(0)}'", sent)

            # 3.6 passive voice (off for Tier C fragments)
            for m in (() if fragments else PASSIVE.finditer(sent)):
                add("3.6", first_ln, f"possible passive voice: '{m.group(0)}'", sent)

            # 3.5 -ing forms.
            # Rule 3.5 permits an "-ing" word used as a technical noun, and the
            # standard names procedural titles and headings as the example case
            # (Cleaning, Handling, Packaging, Shipping, Troubleshooting).  So a
            # single-word "-ing" heading is legal and must NOT be flagged.  Only
            # a gerund PHRASE in a heading ("Getting Started", "Building from
            # Source") is worth reporting, and only as advice.
            if is_heading:
                words = sent.split()
                if len(words) > 1 and re.fullmatch(r"\w+ing", words[0], re.I):
                    add("3.5?", first_ln,
                        f"gerund phrase heading '{sent}' — a bare process noun "
                        f"('{words[0]}') is legal; renaming breaks anchors, so "
                        f"change only after grepping for the old anchor", sent)
            else:
                for m in re.finditer(r"\b(\w+ing)\b", sent):
                    w = m.group(1).lower()
                    if w in ING_ALLOW or len(w) < 5:
                        continue
                    add("3.5", first_ln, f"'-ing' form '{m.group(1)}'", sent)

            # GR-4 bare "This"
            if re.match(r"^This\s+(is|was|will|can|means|produces|makes|gives|lets|does|allows)\b", sent):
                add("GR-4", first_ln, "sentence starts with a bare 'This'", sent)

            # banned words / phrases
            low = " " + sent.lower() + " "
            for bad, good in BANNED.items():
                if re.search(r"(?<![\w-])" + re.escape(bad) + r"(?![\w-])", low):
                    add("word", first_ln, f"'{bad}' -> {good}", sent)

            # 9.3 phrasal verbs
            for bad, good in PHRASAL.items():
                if re.search(r"(?<![\w-])" + re.escape(bad) + r"(?![\w-])", low):
                    add("9.3", first_ln, f"phrasal verb '{bad}' -> {good}", sent)

            # 2.1 multi-word noun runs (heuristic: 4+ capitalized/technical words)
            run = re.search(
                r"\b(?:[a-z]+(?:-[a-z]+)?\s+){3,}(?:[a-z]+(?:s|ing|tion|ment|ance)\b)",
                sent)
            if run and len(run.group(0).split()) >= 5:
                words = run.group(0).split()
                if all(w not in ("the", "a", "an", "of", "to", "in", "on", "for",
                                 "and", "or", "that", "with", "from", "is", "are",
                                 "you", "it", "this", "when", "if", "at", "by",
                                 "as", "can", "not", "all", "its", "which", "then")
                       for w in words):
                    add("2.1", first_ln,
                        f"possible long multi-word noun: '{run.group(0).strip()}'", sent)

    return issues


def summarize(issues):
    by = {}
    for i in issues:
        by[i["rule"]] = by.get(i["rule"], 0) + 1
    return dict(sorted(by.items(), key=lambda kv: -kv[1]))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--tier", default="B", choices=["A", "B", "C", "D", "E"],
                    help="conformance tier: A=procedure/20w, B=description/25w, "
                         "C=reference, D=voice (terminology only), E=frozen")
    ap.add_argument("--limit", type=int, default=None,
                    help="override the sentence word limit")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="summary only")
    ap.add_argument("--max-issues", type=int, default=None,
                    help="exit 1 if any file exceeds this count (CI gate)")
    args = ap.parse_args()

    results, worst = {}, 0
    for f in args.files:
        issues = check(f, args.tier, args.limit)
        results[f] = issues
        worst = max(worst, len(issues))

    if args.json:
        print(json.dumps({k: {"count": len(v), "by_rule": summarize(v),
                              "issues": v} for k, v in results.items()}, indent=2))
    else:
        for f, issues in results.items():
            print(f"\n=== {f} — {len(issues)} issues (tier {args.tier}) ===")
            for rule, n in summarize(issues).items():
                print(f"  {rule:6} {n}")
            if not args.quiet:
                for i in issues:
                    print(f"    {i['rule']:6} line {i['line']:4}  {i['message']}")
                    if i["snippet"]:
                        print(f"             | {i['snippet']}")

    if args.max_issues is not None and worst > args.max_issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
