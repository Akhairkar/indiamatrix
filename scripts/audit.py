import datetime
import json
import math
import os
import sys


def main():
    print("Starting comprehensive data audit...")
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sources_path = os.path.join(root_dir, "data", "sources.json")
    indicators_dir = os.path.join(root_dir, "data", "indicators")
    districts_dir = os.path.join(root_dir, "data", "districts")
    report_path = os.path.join(root_dir, "validation_report.md")
    current_year = datetime.datetime.now(datetime.timezone.utc).year
    errors = []

    if not os.path.exists(sources_path):
        write_report_and_exit(report_path, [f"CRITICAL: {sources_path} is missing."])
    try:
        with open(sources_path, "r", encoding="utf-8") as f:
            sources_data = json.load(f)
        valid_source_ids = {s.get("id") for s in sources_data.get("sources", [])
                            if isinstance(s, dict) and s.get("id")}
    except Exception as exc:
        write_report_and_exit(report_path, [f"CRITICAL: Error reading sources.json: {exc}"])

    def audit_file(filepath, filename):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and isinstance(data.get("indicators"), list):
                indicators = data["indicators"]
            elif isinstance(data, dict) and "id" in data and "value" in data:
                indicators = [data]
            else:
                # History/metadata JSON is not an indicator record.
                return

            seen_ids = set()
            for index, ind in enumerate(indicators):
                label = f"{filename} record {index + 1}"
                if not isinstance(ind, dict):
                    errors.append(f"[{label}] Indicator record must be a JSON object.")
                    continue
                ind_id = ind.get("id", "unknown")
                if ind_id in seen_ids:
                    errors.append(f"[{filename}] Duplicate indicator ID found: '{ind_id}'")
                seen_ids.add(ind_id)

                for field in ("id", "category", "source_id", "source_url", "year", "value", "unit", "display"):
                    if field not in ind:
                        errors.append(f"[{label}] Indicator '{ind_id}' is missing required field '{field}'")

                value = ind.get("value")
                if not isinstance(value, (int, float)) or isinstance(value, bool):
                    errors.append(f"[{label}] Indicator '{ind_id}' has non-numeric value: {value}")
                    numeric_value = None
                elif not math.isfinite(value):
                    errors.append(f"[{label}] Indicator '{ind_id}' has non-finite value: {value}")
                    numeric_value = None
                else:
                    numeric_value = value

                year = ind.get("year")
                if isinstance(year, bool) or not isinstance(year, int) or year < 1900 or year > current_year + 1:
                    errors.append(f"[{label}] Indicator '{ind_id}' has invalid year: {year}")

                unit = ind.get("unit")
                if not isinstance(unit, str) or not unit.strip():
                    errors.append(f"[{label}] Indicator '{ind_id}' has invalid unit: '{unit}'")

                source_id = ind.get("source_id")
                if source_id not in valid_source_ids:
                    errors.append(f"[{label}] Indicator '{ind_id}' has unregistered source_id: '{source_id}'")

                source_url = ind.get("source_url")
                if not isinstance(source_url, str) or not source_url.startswith(("https://", "http://")):
                    errors.append(f"[{label}] Indicator '{ind_id}' has invalid source_url: '{source_url}'")

                display = ind.get("display")
                if not isinstance(display, dict) or not display.get("en") or not display.get("hi"):
                    errors.append(f"[{label}] Indicator '{ind_id}' needs English and Hindi display values")

                if numeric_value is not None:
                    if unit == "%" and not 0 <= numeric_value <= 100:
                        errors.append(f"[{label}] Indicator '{ind_id}' uses '%' but value {numeric_value} is outside 0–100")
                    if ind_id in ("life-expectancy", "life_expectancy") and not 40 <= numeric_value <= 100:
                        errors.append(f"[{label}] Indicator '{ind_id}' has implausible value {numeric_value}")
                    if numeric_value < 0 and "growth" not in str(ind_id).lower():
                        errors.append(f"[{label}] Indicator '{ind_id}' has unexpected negative value {numeric_value}")
        except Exception as exc:
            errors.append(f"CRITICAL: Error reading {filename}: {exc}")

    # Recursively inspect nested indicator folders, including World Bank single-record files.
    for data_dir in (indicators_dir, districts_dir):
        if not os.path.isdir(data_dir):
            continue
        for dirpath, _, filenames in os.walk(data_dir):
            for filename in sorted(filenames):
                if filename.endswith(".json"):
                    filepath = os.path.join(dirpath, filename)
                    relative_name = os.path.relpath(filepath, root_dir).replace(os.sep, "/")
                    audit_file(filepath, relative_name)

    if errors:
        write_report_and_exit(report_path, errors)
    if os.path.exists(report_path):
        os.remove(report_path)
    print("Audit passed: all discovered indicator records satisfy the configured data rules.")
    sys.exit(0)


def write_report_and_exit(report_path, errors):
    print(f"Audit failed with {len(errors)} errors. Writing report to validation_report.md...")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Data Validation Report\n\n")
        f.write(f"**Generated at:** {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n\n")
        f.write("The automated data pipeline was halted due to the following validation errors:\n\n")
        for error in errors:
            f.write(f"- {error}\n")
    print(f"Validation report saved to {report_path}")
    sys.exit(1)


if __name__ == "__main__":
    main()
