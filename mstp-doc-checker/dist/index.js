/**
 * Doc Style Checker — MCP Server
 * ==============================
 * Reviews HTML documentation (e.g., output of a JSON-to-HTML conversion skill)
 * against a chosen style guide — Microsoft (default), IBM, or Google — plus
 * general documentation rules and HTML structure checks.
 *
 * TOOLS
 *  1. check_writing_style  — style-guide-aware prose checks. Pass
 *                            style_guide: "microsoft" | "ibm" | "google".
 *  2. check_html_structure — unclosed/mismatched tags, duplicate IDs,
 *                            missing DOCTYPE and <title>.
 *  3. check_general_rules  — rules that apply regardless of style guide:
 *                            conversion leftovers ("undefined", "null",
 *                            "[object Object]", {{placeholders}}), empty
 *                            elements, semantic-HTML5 hints.
 *  4. run_quality_report   — all three checks in one scored report.
 *
 * RESOURCE
 *  styleguide://main — serves resources/styleguide.md (the full rulebook),
 *  so the model can read the complete guide for judgment-based review of
 *  things code can't measure (clarity, tone, global audience, and so on).
 *
 * Each tool accepts EITHER:
 *   file_path : absolute path to an .html file, OR
 *   html      : a raw HTML string.
 */
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
/* ---------------- Server setup ---------------- */
const server = new McpServer({
    name: "doc-style-checker",
    version: "2.0.0",
});
/** Folder this compiled file lives in (dist/), used to find resources/. */
const HERE = dirname(fileURLToPath(import.meta.url));
const STYLEGUIDE_PATH = join(HERE, "..", "resources", "styleguide.md");
const VOID_ELEMENTS = new Set([
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
]);
function loadHtml(filePath, html) {
    if (html && html.trim().length > 0)
        return { html, label: "(inline HTML)" };
    if (filePath && filePath.trim().length > 0)
        return { html: readFileSync(filePath, "utf-8"), label: filePath };
    throw new Error("Provide either 'file_path' or 'html'.");
}
function lineOf(text, index) {
    return text.slice(0, index).split("\n").length;
}
/** Blank out comments, scripts, styles — keep line breaks so line numbers stay right. */
function stripNonContent(html) {
    const blank = (m) => m.replace(/[^\n]/g, " ");
    return html
        .replace(/<!--[\s\S]*?-->/g, blank)
        .replace(/<script[\s\S]*?<\/script>/gi, blank)
        .replace(/<style[\s\S]*?<\/style>/gi, blank);
}
/** Also blank out code samples — writing-style rules apply to prose, not code. */
function proseOnly(html) {
    const blank = (m) => m.replace(/[^\n]/g, " ");
    return stripNonContent(html)
        .replace(/<pre[\s\S]*?<\/pre>/gi, blank)
        .replace(/<code[\s\S]*?<\/code>/gi, blank);
}
function formatIssues(title, label, issues) {
    const e = issues.filter(i => i.severity === "error");
    const w = issues.filter(i => i.severity === "warning");
    const n = issues.filter(i => i.severity === "info");
    const out = [];
    out.push(title, `Document: ${label}`, `Result: ${e.length} error(s), ${w.length} warning(s), ${n.length} note(s)`, "");
    for (const i of [...e, ...w, ...n]) {
        out.push(`  [${i.severity.toUpperCase()}]${i.line ? ` line ${i.line}:` : ""} ${i.message}`);
    }
    if (issues.length === 0)
        out.push("  ✔ No issues found.");
    return out.join("\n");
}
function scoreFromIssues(issues) {
    const penalty = issues.reduce((a, i) => a + (i.severity === "error" ? 15 : i.severity === "warning" ? 5 : 1), 0);
    return Math.max(0, 100 - penalty);
}
/**
 * Rules shared by ALL three guides (they agree on these).
 * TO ADD YOUR OWN RULE: copy a line, change the pattern and the message.
 */
const SHARED_RULES = [
    { re: /\bclick on\b/gi, severity: "warning", msg: `Use "select" (or just "click") instead of "click on".` },
    { re: /\be\.g\.\b/gi, severity: "warning", msg: `Use "for example" instead of "e.g.".` },
    { re: /\bi\.e\.\b/gi, severity: "warning", msg: `Use "that is" instead of "i.e.".` },
    { re: /\betc\.?(?=\s|$)/gi, severity: "warning", msg: `Avoid "etc." — use "and so on", or complete the list.` },
    { re: /\butiliz(e|es|ed|ing)\b/gi, severity: "warning", msg: `Use "use" instead of "utilize".` },
    { re: /\bleverage\b/gi, severity: "info", msg: `Prefer "use" instead of "leverage".` },
    { re: /\bin order to\b/gi, severity: "info", msg: `Shorten "in order to" to "to".` },
    { re: /\bprior to\b/gi, severity: "info", msg: `Use "before" instead of "prior to".` },
    { re: /\bvia\b/gi, severity: "info", msg: `Prefer "by using" or "through" instead of "via".` },
    { re: /\babort(ed|ing|s)?\b/gi, severity: "warning", msg: `Use "stop" or "cancel" instead of "abort".` },
    { re: /\bkill(ed|ing|s)?\b/gi, severity: "warning", msg: `Use "stop" or "end" instead of "kill".` },
    { re: /\bwill (be|display|show|appear|open|create|generate|return)\b/gi, severity: "info", msg: `Use present tense where possible ("appears", not "will appear").` },
];
/** Rules specific to each guide. */
const GUIDE_RULES = {
    microsoft: [
        { re: /\bplease\b/gi, severity: "warning", msg: `Microsoft style: avoid "please" in instructions — just state the action.` },
        { re: /\bcannot\b/gi, severity: "info", msg: `Microsoft style encourages contractions: use "can't".` },
        { re: /\bdo not\b/gi, severity: "info", msg: `Microsoft style encourages contractions: use "don't".` },
        { re: /\bwe recommend\b/gi, severity: "info", msg: `Microsoft style prefers direct address: "You should..." or state the action.` },
    ],
    ibm: [
        { re: /\b(can't|don't|won't|isn't|aren't|doesn't|didn't|couldn't|shouldn't|wouldn't)\b/gi, severity: "info", msg: `IBM style avoids contractions in formal documentation — spell it out.` },
        { re: /\b(a lot of|lots of)\b/gi, severity: "warning", msg: `IBM style: avoid colloquial phrasing — use "many" or "much".` },
        { re: /\b(stuff|things)\b/gi, severity: "info", msg: `IBM style: avoid vague colloquial words — name the items specifically.` },
    ],
    google: [
        { re: /\bplease\b/gi, severity: "warning", msg: `Google style: avoid "please" in instructions — just state the action.` },
        { re: /\bcannot\b/gi, severity: "info", msg: `Google style encourages contractions: use "can't".` },
        { re: /\bsimply\b/gi, severity: "info", msg: `Google style: avoid "simply" — it can frustrate readers when the task isn't simple for them.` },
        { re: /\beasy|easily\b/gi, severity: "info", msg: `Google style: avoid claiming things are "easy" — write for a global audience of all skill levels.` },
    ],
};
function checkWritingStyle(html, guide) {
    const issues = [];
    const prose = proseOnly(html);
    const rules = [...SHARED_RULES, ...GUIDE_RULES[guide]];
    // (a) Word and phrase rules for the selected guide.
    for (const rule of rules) {
        rule.re.lastIndex = 0; // reset between runs
        let m;
        while ((m = rule.re.exec(prose)) !== null) {
            issues.push({ severity: rule.severity, line: lineOf(prose, m.index), message: `${rule.msg} (found: "${m[0]}")` });
        }
    }
    // (b) First person — all three guides prefer second person ("you").
    const firstPerson = /\b(we|our|us)\b/gi;
    let fp;
    while ((fp = firstPerson.exec(prose)) !== null) {
        issues.push({ severity: "info", line: lineOf(prose, fp.index), message: `First person "${fp[0]}" — prefer second person ("you", "your").` });
    }
    // (c) Possible passive voice — a simple heuristic; review flagged lines yourself.
    const passive = /\b(is|are|was|were|be|been|being)\s+(\w+ed)\b/gi;
    let pv;
    while ((pv = passive.exec(prose)) !== null) {
        issues.push({ severity: "info", line: lineOf(prose, pv.index), message: `Possible passive voice: "${pv[0]}" — prefer active voice.` });
    }
    // (d) Headings should be sentence case (all three guides agree).
    const cleaned = stripNonContent(html);
    const headingRe = /<h([1-6])\b[^>]*>([\s\S]*?)<\/h\1>/gi;
    let h;
    while ((h = headingRe.exec(cleaned)) !== null) {
        const text = h[2].replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
        const words = text.split(" ").slice(1); // skip the first word
        const titleCased = words.filter(w => /^[A-Z][a-z]/.test(w));
        if (titleCased.length >= 2) {
            issues.push({ severity: "warning", line: lineOf(cleaned, h.index), message: `Heading "${text}" looks like Title Case — use sentence case. (Ignore if these are product names.)` });
        }
    }
    // (e) Google only: flag very long sentences (global-audience readability).
    if (guide === "google") {
        const text = prose.replace(/<[^>]+>/g, " ");
        const sentenceRe = /[^.!?]*[.!?]/g;
        let s;
        while ((s = sentenceRe.exec(text)) !== null) {
            const wordCount = s[0].trim().split(/\s+/).filter(Boolean).length;
            if (wordCount > 30) {
                issues.push({ severity: "info", line: lineOf(text, s.index), message: `Sentence with ${wordCount} words — Google style prefers short sentences; consider splitting it.` });
            }
        }
    }
    return issues;
}
/* ---------------- General documentation rules ---------------- */
function checkGeneralRules(html) {
    const issues = [];
    const cleaned = stripNonContent(html);
    // (a) Conversion leftovers — signs a JSON field failed to render.
    const artifacts = [
        { re: />\s*undefined\s*</g, severity: "error", msg: `Literal "undefined" rendered as content — a JSON field likely failed to resolve.` },
        { re: />\s*null\s*</g, severity: "error", msg: `Literal "null" rendered as content — a JSON field was null and not handled.` },
        { re: /\[object Object\]/g, severity: "error", msg: `"[object Object]" found — an object was stringified instead of its property being read.` },
        { re: /\{\{[^}]*\}\}/g, severity: "error", msg: "Unresolved {{template placeholder}} left in the output." },
        { re: /\b(TODO|FIXME|TBD)\b/g, severity: "error", msg: "Placeholder marker (TODO/FIXME/TBD) present in content." },
        { re: /lorem ipsum/gi, severity: "error", msg: "Lorem ipsum filler text present in content." },
    ];
    for (const a of artifacts) {
        a.re.lastIndex = 0;
        let m;
        while ((m = a.re.exec(cleaned)) !== null) {
            issues.push({ severity: a.severity, line: lineOf(cleaned, m.index), message: a.msg });
        }
    }
    // (b) Empty content elements — a section rendered with no value.
    for (const tag of ["h1", "h2", "h3", "h4", "p", "li", "td", "th", "a"]) {
        const re = new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)<\\/${tag}>`, "gi");
        let m;
        while ((m = re.exec(cleaned)) !== null) {
            const text = m[1].replace(/<[^>]+>/g, "").replace(/\s+/g, " ").trim();
            if (text.length === 0) {
                issues.push({ severity: "warning", line: lineOf(cleaned, m.index), message: `Empty <${tag}> element — the source JSON value may be missing.` });
            }
        }
    }
    // (c) Semantic HTML5 hint — long docs built only from <div> blocks.
    const divCount = (cleaned.match(/<div\b/gi) || []).length;
    const semanticCount = (cleaned.match(/<(main|section|article|nav|header|footer|aside)\b/gi) || []).length;
    if (divCount >= 5 && semanticCount === 0) {
        issues.push({ severity: "info", message: `Document uses ${divCount} <div> elements and no semantic HTML5 elements (<main>, <section>, <article>...) — prefer semantic markup.` });
    }
    return issues;
}
/* ---------------- HTML structure ---------------- */
function checkStructure(html) {
    const issues = [];
    const cleaned = stripNonContent(html);
    if (!/^\s*<!doctype\s+html/i.test(html))
        issues.push({ severity: "warning", message: "Missing <!DOCTYPE html> at the top." });
    if (!/<title\b[^>]*>\s*\S/i.test(cleaned))
        issues.push({ severity: "warning", message: "Missing or empty <title> in <head>." });
    // Tag balance using a stack.
    const stack = [];
    const tagRe = /<\s*(\/?)\s*([a-zA-Z][a-zA-Z0-9-]*)((?:"[^"]*"|'[^']*'|[^>"'])*)>/g;
    let t;
    while ((t = tagRe.exec(cleaned)) !== null) {
        const name = t[2].toLowerCase();
        const closing = t[1] === "/";
        const selfClosing = /\/\s*$/.test(t[3]);
        if (VOID_ELEMENTS.has(name) || selfClosing)
            continue;
        if (!closing) {
            stack.push({ name, index: t.index });
            continue;
        }
        if (stack.length && stack[stack.length - 1].name === name) {
            stack.pop();
            continue;
        }
        const at = stack.map(s => s.name).lastIndexOf(name);
        if (at === -1) {
            issues.push({ severity: "error", line: lineOf(cleaned, t.index), message: `Closing </${name}> has no matching opening tag.` });
        }
        else {
            for (let i = stack.length - 1; i > at; i--)
                issues.push({ severity: "error", line: lineOf(cleaned, stack[i].index), message: `<${stack[i].name}> was never closed.` });
            stack.length = at;
        }
    }
    for (const s of stack)
        issues.push({ severity: "error", line: lineOf(cleaned, s.index), message: `<${s.name}> opened but never closed.` });
    // Duplicate IDs.
    const seen = new Map();
    const idRe = /\bid\s*=\s*["']([^"']+)["']/gi;
    let im;
    while ((im = idRe.exec(cleaned)) !== null) {
        if (seen.has(im[1]))
            issues.push({ severity: "error", line: lineOf(cleaned, im.index), message: `Duplicate id "${im[1]}" (first used line ${seen.get(im[1])}).` });
        else
            seen.set(im[1], lineOf(cleaned, im.index));
    }
    return issues;
}
/* ---------------- Register the resource ---------------- */
server.resource("styleguide", "styleguide://main", { description: "The full documentation style guide (Microsoft, IBM, Google, and general rules). Read this when doing a judgment-based review of tone, clarity, and structure that the mechanical tools can't measure.", mimeType: "text/markdown" }, async (uri) => ({
    contents: [{ uri: uri.href, mimeType: "text/markdown", text: readFileSync(STYLEGUIDE_PATH, "utf-8") }],
}));
/* ---------------- Register the tools ---------------- */
const inputSchema = {
    file_path: z.string().optional().describe("Absolute path to the HTML file to review."),
    html: z.string().optional().describe("Raw HTML string to review (alternative to file_path)."),
    style_guide: z.enum(["microsoft", "ibm", "google"]).optional()
        .describe("Which style guide to check against. Defaults to 'microsoft' if not specified."),
};
server.tool("check_writing_style", "Reviews the prose of an HTML doc against the selected style guide (microsoft = default, ibm, or google): sentence-case headings, second person, active voice, present tense, plain words, and guide-specific rules like contractions (encouraged by Microsoft/Google, avoided by IBM) and sentence length (Google). Code samples are ignored.", inputSchema, async ({ file_path, html, style_guide }) => {
    const guide = style_guide ?? "microsoft";
    const { html: doc, label } = loadHtml(file_path, html);
    return { content: [{ type: "text", text: formatIssues(`WRITING STYLE CHECK (${guide.toUpperCase()} style)`, label, checkWritingStyle(doc, guide)) }] };
});
server.tool("check_html_structure", "Checks an HTML document for well-formedness: unclosed or mismatched tags, duplicate IDs, missing DOCTYPE and <title>.", inputSchema, async ({ file_path, html }) => {
    const { html: doc, label } = loadHtml(file_path, html);
    return { content: [{ type: "text", text: formatIssues("HTML STRUCTURE CHECK", label, checkStructure(doc)) }] };
});
server.tool("check_general_rules", "Checks rules that apply regardless of style guide: leftover conversion artifacts (literal 'undefined'/'null'/'[object Object]', unresolved {{placeholders}}, TODO markers, lorem ipsum), empty headings/paragraphs/cells/links, and semantic-HTML5 usage. Run this on every file produced by JSON-to-HTML conversion.", inputSchema, async ({ file_path, html }) => {
    const { html: doc, label } = loadHtml(file_path, html);
    return { content: [{ type: "text", text: formatIssues("GENERAL DOCUMENTATION RULES CHECK", label, checkGeneralRules(doc)) }] };
});
server.tool("run_quality_report", "Runs all three checks (writing style for the selected guide, HTML structure, general documentation rules) and returns one combined report with a 0-100 score per area and an overall grade. style_guide defaults to 'microsoft'.", inputSchema, async ({ file_path, html, style_guide }) => {
    const guide = style_guide ?? "microsoft";
    const { html: doc, label } = loadHtml(file_path, html);
    const areas = [
        { name: `Writing style (${guide})`, issues: checkWritingStyle(doc, guide) },
        { name: "HTML structure", issues: checkStructure(doc) },
        { name: "General rules", issues: checkGeneralRules(doc) },
    ];
    const scored = areas.map(a => ({ ...a, score: scoreFromIssues(a.issues) }));
    const overall = Math.round(scored.reduce((s, a) => s + a.score, 0) / scored.length);
    const grade = overall >= 90 ? "A" : overall >= 80 ? "B" : overall >= 70 ? "C" : overall >= 60 ? "D" : "F";
    const out = ["DOC QUALITY REPORT", `Document: ${label}`, `Style guide: ${guide}`, `Overall: ${overall}/100 (Grade ${grade})`, ""];
    for (const a of scored) {
        out.push(`── ${a.name}: ${a.score}/100 ──`);
        if (a.issues.length === 0)
            out.push("  ✔ No issues.");
        for (const i of a.issues)
            out.push(`  [${i.severity.toUpperCase()}]${i.line ? ` line ${i.line}:` : ""} ${i.message}`);
        out.push("");
    }
    out.push("Scoring: error -15, warning -5, note -1 (floor 0).");
    return { content: [{ type: "text", text: out.join("\n") }] };
});
/* ---------------- Start the server ---------------- */
const transport = new StdioServerTransport();
await server.connect(transport);
// Never use console.log() here — it would corrupt the MCP message stream.
console.error("doc-style-checker MCP server running on stdio");
