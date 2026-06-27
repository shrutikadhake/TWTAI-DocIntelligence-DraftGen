import json, os, re, shutil

BASE = r"C:\Users\HP\Doc-Intelligence\TWTAI-DocIntelligence-DraftGen\md-to-html-workspace\iteration-1"

EVALS = [
    ("eval-relative-path",  ["with_skill", "without_skill"]),
    ("eval-filename-only",  ["with_skill", "without_skill"]),
    ("eval-absolute-path",  ["with_skill", "without_skill"]),
]

def check(html):
    return {
        "has-doctype":       ("<!DOCTYPE html>" in html, "Found <!DOCTYPE html>" if "<!DOCTYPE html>" in html else "Missing <!DOCTYPE html>"),
        "has-meta-charset":  (re.search(r'<meta\s+charset=["\']UTF-8["\']', html, re.I) is not None,
                              "Found meta charset UTF-8" if re.search(r'<meta\s+charset=["\']UTF-8["\']', html, re.I) else "Missing meta charset UTF-8"),
        "title-from-h1":     ("<title>Payment Gateway API</title>" in html,
                              "Correct title tag" if "<title>Payment Gateway API</title>" in html else "Missing or wrong title"),
        "h1-converted":      ("<h1>Payment Gateway API</h1>" in html,
                              "h1 found" if "<h1>Payment Gateway API</h1>" in html else "Missing h1"),
        "h2-converted":      ("<h2>" in html, "h2 tags present" if "<h2>" in html else "No h2 tags"),
        "h3-converted":      ("<h3>" in html, "h3 tags present" if "<h3>" in html else "No h3 tags"),
        "bold-converted":    ("<strong>" in html, "<strong> present" if "<strong>" in html else "No <strong> tags"),
        "fenced-code-block": ("<pre><code>" in html, "<pre><code> present" if "<pre><code>" in html else "No <pre><code> blocks"),
        "table-structure":   (all(t in html for t in ["<table>","<thead>","<tbody>","<th>","<td>"]),
                              "Full table structure present" if all(t in html for t in ["<table>","<thead>","<tbody>","<th>","<td>"]) else
                              f"Missing: {[t for t in ['<table>','<thead>','<tbody>','<th>','<td>'] if t not in html]}"),
        "bullet-list":       (("<ul>" in html and "<li>" in html), "<ul> and <li> present" if ("<ul>" in html and "<li>" in html) else "Missing ul/li"),
        "numbered-list":     (("<ol>" in html and "<li>" in html), "<ol> and <li> present" if ("<ol>" in html and "<li>" in html) else "Missing ol/li"),
        "blockquote-converted": ("<blockquote>" in html, "<blockquote> present" if "<blockquote>" in html else "No blockquote"),
        "hr-converted":      ("<hr>" in html, "<hr> present" if "<hr>" in html else "No <hr>"),
        "image-converted":   ('<img src="https://via.placeholder.com' in html,
                              "img tag with correct src" if '<img src="https://via.placeholder.com' in html else "Missing or wrong img tag"),
        "links-converted":   ("<a href=" in html, "<a href= present" if "<a href=" in html else "No links"),
        "no-css":            ("<style>" not in html and "style=" not in html,
                              "No CSS found" if ("<style>" not in html and "style=" not in html) else "CSS detected"),
        "output-filename":   (True, "Checked by file path"),
        "body-tag":          ("<body>" in html, "<body> present" if "<body>" in html else "No <body> tag"),
    }

for eval_name, configs in EVALS:
    for config in configs:
        html_path = os.path.join(BASE, eval_name, config, "outputs", "sample-doc.html")
        timing_path = os.path.join(BASE, eval_name, config, "timing.json")

        # Create run-1 subdirectory
        run_dir = os.path.join(BASE, eval_name, config, "run-1")
        os.makedirs(run_dir, exist_ok=True)

        run_grading_path = os.path.join(run_dir, "grading.json")
        run_timing_path = os.path.join(run_dir, "timing.json")

        if not os.path.exists(html_path):
            print(f"MISSING: {html_path}")
            continue
        with open(html_path, encoding="utf-8") as f:
            html = f.read()
        results = check(html)
        expectations = [
            {"text": aid, "passed": passed, "evidence": evidence}
            for aid, (passed, evidence) in results.items()
        ]
        passed_count = sum(1 for _, (p, _) in results.items() if p)
        total = len(results)
        grading = {
            "expectations": expectations,
            "summary": {
                "passed": passed_count,
                "failed": total - passed_count,
                "total": total,
                "pass_rate": round(passed_count / total, 4)
            }
        }
        with open(run_grading_path, "w", encoding="utf-8") as f:
            json.dump(grading, f, indent=2)

        # Copy timing.json to run-1/
        if os.path.exists(timing_path):
            shutil.copy2(timing_path, run_timing_path)

        print(f"{eval_name}/{config}: {passed_count}/{total} passed ({100*passed_count//total}%)")

print("Done.")
