from forge.agents.web_auditor import audit


def write(root, name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_web_auditor_analyzes_js_and_ts_and_reports_high_signal_patterns(tmp_path):
    write(tmp_path, "main.ts", "export function parse(raw: string) { return JSON.parse(raw); }\n")
    write(tmp_path, "worker.js", "const run = (cmd) => child_process.exec(cmd);\n")
    result, analyzed = audit(tmp_path)
    assert set(analyzed) == {"main.ts", "worker.js"}
    assert {(item.path, item.family) for item in result.findings} == {
        ("main.ts", "parser-boundary"),
        ("worker.js", "subprocess"),
    }


def test_web_auditor_does_not_call_database_exec_a_subprocess(tmp_path):
    write(tmp_path, "query.ts", "const result = db.exec(statement);\n")
    result, _ = audit(tmp_path)
    assert not [item for item in result.findings if item.family == "subprocess"]


def test_web_auditor_does_not_flag_json_parse_with_visible_boundary(tmp_path):
    write(tmp_path, "safe.ts", """
try {
  const data = JSON.parse(raw);
} catch (error) {
  return fallback(error);
}
""")
    result, analyzed = audit(tmp_path)
    assert analyzed == ("safe.ts",)
    assert not result.findings


def test_web_auditor_handles_comments_as_non_executable_text(tmp_path):
    write(tmp_path, "notes.ts", "// eval(userInput)\nconst label = 'JSON.parse(raw)';\n")
    result, _ = audit(tmp_path)
    assert not result.findings


def test_web_auditor_masks_unterminated_minified_literals_in_linear_time(tmp_path):
    write(tmp_path, "pathological.js", "const payload = `" + ("x" * 100_000) + "\n")
    result, analyzed = audit(tmp_path)
    assert analyzed == ("pathological.js",)
    assert not result.findings


def test_web_auditor_excludes_generated_next_artifacts(tmp_path):
    write(tmp_path, ".next/static/chunk.js", "eval(userInput);\n")
    write(tmp_path, "src/app.ts", "export const app = true;\n")
    result, analyzed = audit(tmp_path)
    assert analyzed == ("src/app.ts",)
    assert not result.findings
