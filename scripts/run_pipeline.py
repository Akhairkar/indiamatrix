import os
import sys
import subprocess
import argparse

# Ensure we can import adapters
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
    else:
        print(f"--> [PASS]: {desc}")

def main():
    parser = argparse.ArgumentParser(description="IndiaMetrix Complete Automated Data Pipeline")
    parser.add_argument("--force", action="store_true", help="Force full rebuild even if no upstream data changed")
    parser.add_argument("--skip-fetch", action="store_true", help="Skip remote fetching and run local verification & build")
    args = parser.parse_args()

    print("==========================================")
    print("      INDIAMETRIX MASTER PIPELINE         ")
    print("==========================================")
    
    data_changed = False
    if not args.skip_fetch:
        adapters = [WorldBankAdapter()]
        for adapter in adapters:
            try:
                if adapter.run():
                    data_changed = True
            except Exception as e:
                print(f"Warning: Adapter {adapter.__class__.__name__} failed: {e}")

    if not data_changed and not args.force and not args.skip_fetch:
        print("\nNo remote data changed. Run with --force or --skip-fetch to execute full validation & build.")
        return

    # 1. Data Integrity & Conflict Detection
    run_command("python scripts/detect_conflicts.py", "Data Conflict & Outlier Detection")

    # 2. Comprehensive Schema & Rule Audit
    run_command("python scripts/audit.py", "Data Verification & Governance Audit")

    # 3. Compile Master Data Stores
    run_command("python scripts/build_rankings.py", "Generate Verified Indicator Rankings")
    run_command("python scripts/build_explorer_data.py", "Compile Explorer, Search & AI Index")

    # 4. Build HTML Pages
    run_command("python scripts/build.py", "Build Static HTML Profiles & Pages")

    # 5. Contextual Internal Linking
    run_command("python scripts/linkify.py", "Contextual Internal Linking Engine")

    # 6. Orphan & Crawlability Audit
    run_command("python scripts/audit_orphans.py", "Internal Link Reachability & Orphan Audit")

    # 7. Sitemap & SEO Indexing
    run_command("python scripts/sitemap.py", "XML Sitemap & Content Value Gate Generation")

    print("\n==========================================")
    print("ALL 7 PIPELINE PHASES PASSED WITH ZERO ERRORS!")
    print("IndiaMetrix is ready for deployment.")
    print("==========================================")

if __name__ == "__main__":
    main()
