import os
import sys
import subprocess
import argparse

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from adapters.worldbank_adapter import WorldBankAdapter


def run_command(cmd, desc):
    print(f"\n==========================================")
    print(f"--> [RUNNING]: {desc}")
    print(f"==========================================")
    result = subprocess.run(cmd, shell=True, text=True)
    if result.returncode != 0:
        print(f"\n[PIPELINE ERROR]: Failure during {desc} (Exit code {result.returncode})")
        sys.exit(result.returncode)
    print(f"--> [PASS]: {desc}")


def run_integrity_checks():
    run_command("python scripts/detect_conflicts.py", "Data Conflict & Outlier Detection")
    run_command("python scripts/audit.py", "Data Verification & Governance Audit")


def run_build_steps():
    run_command("python scripts/build_rankings.py", "Generate Verified Indicator Rankings")
    run_command("python scripts/build_explorer_data.py", "Compile Explorer, Search & AI Index")
    run_command("python scripts/build.py", "Build Static HTML Profiles & Pages")
    run_command("python scripts/linkify.py", "Contextual Internal Linking Engine")
    run_command("python scripts/audit_orphans.py", "Internal Link Reachability & Orphan Audit")
    run_command("python scripts/sitemap.py", "XML Sitemap & Content Value Gate Generation")


def main():
    parser = argparse.ArgumentParser(description="IndiaMetrix Complete Automated Data Pipeline")
    parser.add_argument("--force", action="store_true", help="Force full rebuild even if no upstream data changed")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip remote fetching and run local verification & build")
    args = parser.parse_args()

    print("==========================================")
    print("      INDIAMETRIX MASTER PIPELINE         ")
    print("==========================================")

    data_changed = False
    adapter_failed = False
    if not args.skip_fetch:
        for adapter in (WorldBankAdapter(),):
            try:
                result = adapter.run()
                if result is None:
                    adapter_failed = True
                elif result:
                    data_changed = True
            except Exception as exc:
                print(f"[PIPELINE ERROR] Adapter {adapter.__class__.__name__} failed: {exc}")
                adapter_failed = True

    if adapter_failed:
        print("[PIPELINE ERROR] One or more data adapters failed; refusing to report a successful update.")
        sys.exit(1)

    # Validate on every scheduled run, including days with no source changes.
    run_integrity_checks()
    if not data_changed and not args.force and not args.skip_fetch:
        print("No remote data changed. Integrity checks passed; skipping page regeneration.")
        return

    run_build_steps()
    print("\n==========================================")
    print("ALL PIPELINE PHASES PASSED.")
    print("IndiaMetrix is ready for deployment.")
    print("==========================================")


if __name__ == "__main__":
    main()
