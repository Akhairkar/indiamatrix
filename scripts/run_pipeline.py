import os
import sys
import subprocess

# Ensure we can import adapters
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from adapters.worldbank_adapter import WorldBankAdapter

def run_command(cmd, desc):
    print(f"\n--- {desc} ---")
    result = subprocess.run(cmd, shell=True, text=True)
    if result.returncode != 0:
        print(f"Error during: {desc}")
        sys.exit(1)
    else:
        print(f"Success: {desc}")

def main():
    print("Starting Automated Data Pipeline...")
    
    # 1. Run Adapters
    adapters = [
        WorldBankAdapter()
    ]
    
    data_changed = False
    for adapter in adapters:
        if adapter.run():
            data_changed = True
            
    if not data_changed:
        print("\nNo new data fetched from any sources. Exiting pipeline.")
        return
        
    print("\nNew data was saved! Triggering rebuild process...")
    
    # 2. Audit new data
    run_command("python scripts/audit.py", "Data Audit")
    
    # 3. Rebuild compiled JSONs
    run_command("python scripts/build_rankings.py", "Build Rankings JSON")
    run_command("python scripts/build_explorer_data.py", "Build Explorer JSON")
    
    # 4. Rebuild HTML
    run_command("python scripts/build.py", "Build HTML Pages")
    run_command("python scripts/sitemap.py", "Generate Sitemap")
    
    print("\nPipeline completed successfully! Site is ready for deployment.")

if __name__ == "__main__":
    main()
