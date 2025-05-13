# main.py (for GitHub Actions)

from generate_wade_draft import run_gpt_fill_pipeline

if __name__ == "__main__":
    print("🚀 Running WADE newsletter filler...")
    try:
        date_str = run_gpt_fill_pipeline()
        print(f"✅ Draft created for {date_str}")
    except Exception as e:
        print("❌ Failed to create draft:")
        print(e)
        raise
