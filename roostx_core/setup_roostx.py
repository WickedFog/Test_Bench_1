import os

# Define the folder structure based on ChatGPT's architecture
structure = [
    "AI_TEAM/prompts",
    "AI_TEAM/responses/gemini",
    "AI_TEAM/responses/claude",
    "AI_TEAM/responses/grok",
    "AI_TEAM/responses/chatgpt",
    "research_database/switch_usage",
    "research_database/crawler_setups",
    "research_database/dig_setups",
    "research_database/winch_setups",
    "research_database/lighting_systems",
    "research_database/telemetry_examples",
    "roostx_core/engine",
    "roostx_core/features",
    "roostx_core/vehicles",
    "radio_maps",
    "docs",
    "test_models/generated",
    "test_models/real_models"
]

# Define placeholder files to keep the structure clean
files = {
    "AI_TEAM/prompts/team_rules.txt": "ROOSTX AI TEAM OPERATING RULES (v1)",
    "docs/roostx_engineering_brief.txt": "Initial engineering brief and architecture goals.",
    "radio_maps/mt12.json": "{}",
    "roostx_core/engine/model.py": "# RoosTX EdgeTX Model Generator Engine",
}

def create_roostx_workspace():
    print("--- Initializing RoosTX Workspace ---")
    
    # Create Directories
    for folder in structure:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

    # Create Initial Files
    for file_path, content in files.items():
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Created file: {file_path}")

    print("\nSUCCESS: RoosTX directory structure is ready.")

if __name__ == "__main__":
    create_roostx_workspace()