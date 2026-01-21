import os

def load_prompt_from_file(filename: str) -> str:
    """Loads a prompt from a file in the prompts directory."""
    # Assuming prompts are in ../prompts relative to this file
    # utils.py is in expense_manager/utils/
    # prompts is in expense_manager/prompts/
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir) # expense_manager
    prompts_dir = os.path.join(project_root, "prompts")
    
    file_path = os.path.join(prompts_dir, filename)
    
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        # Fallback or error
        raise FileNotFoundError(f"Prompt file not found: {file_path}")