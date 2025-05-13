# generate_draft_modular.py

from generate_wade_draft import run_gpt_fill_pipeline_minimal
from post_to_zapier import post_to_substack_zap

def main():
    print("🚀 Generating WADE newsletter draft...")
    try:
        draft = run_gpt_fill_pipeline_minimal()

        # Assemble Markdown
        body = "\n\n".join(
            f"## {header}\n{content}" for header, content in draft["sections"].items()
        )

        post_to_substack_zap(title=draft["title"], content=body)
        print("✅ Draft sent to Zapier.")
    except Exception as e:
        print("❌ Error generating WADE draft:", e)

if __name__ == "__main__":
    main()
