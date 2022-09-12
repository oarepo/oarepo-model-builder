from collections import defaultdict


def assert_python_equals(actual, expected, msg=""):
    actual_lines = [x.strip() for x in actual.split("\n")]
    expected_lines = [x.strip() for x in expected.split("\n")]

    expected_by_content = defaultdict(list)
    for lineno, line in enumerate(expected_lines):
        line = line.strip()
        if not line:
            continue
        expected_by_content[line].append(lineno)

    last_line = 0
    for actual_line_no, actual_line in enumerate(actual_lines):
        actual_line = actual_line.strip()
        if not actual_line:
            continue
        if actual_line in expected_by_content and expected_by_content[actual_line]:
            last_line = expected_by_content[actual_line].pop(0)
        else:
            print("Expected lines:\n")
            print_lines_around(expected_lines, last_line)

            print("Actual lines:\n")
            print_lines_around(actual_lines, actual_line_no)

            raise AssertionError(
                f"Actual line {actual_line_no + 1} '{actual_line}' not in expected lines. {msg}"
            )


def print_lines_around(lines, position):
    for p in range(max(0, position - 10), min(len(lines), position + 11)):
        print(f"{str(p + 1):5s} {lines[p]}")
