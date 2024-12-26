import re
from pathlib import Path
from mkdocs.config import config_options, base

class WorkExperienceConfig(base.Config):
    docs_dir = config_options.Type(str, default='docs')  # Default if not in MkDocs

def on_env(env, config, files):
    """Register the get_work_experience function with the template environment"""
    env.globals['get_work_experience'] = lambda: get_work_experience(config)
    return env

def parse_markdown_content(content):
    experiences = []
    current_company = None
    current_roles = []
    
    # Split content by sections and filter out empty lines
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Company section starts with ###
        if line.startswith('### '):
            # Process previous company if exists
            if current_company and current_roles:
                if len(current_roles) == 1:
                    role = current_roles[0]
                    experiences.append({
                        "company": current_company,
                        "role": role["title"],
                        "start_date": role["start_date"],
                        "end_date": role["end_date"],
                        "responsibilities": role["responsibilities"]
                    })
                else:
                    experiences.append({
                        "company": current_company,
                        "roles": current_roles
                    })
            
            # Start new company
            current_company = line.replace('### ', '').strip()
            current_roles = []
        
        # Role section starts with ####
        elif line.startswith('#### '):
            role = {
                "title": line.replace('#### ', '').strip(),
                "start_date": "",
                "end_date": "",
                "responsibilities": []
            }
            
            # Look ahead for dates and responsibilities
            i += 1
            if i < len(lines):
                date_line = lines[i]
                if '*' in date_line:
                    date_parts = date_line.strip('*').split('-')
                    role["start_date"] = date_parts[0].strip()
                    role["end_date"] = date_parts[1].strip()
                    
                    # Get responsibilities
                    i += 1
                    while i < len(lines) and lines[i].startswith('- '):
                        resp = lines[i].replace('- ', '').strip()
                        role["responsibilities"].append(resp)
                        i += 1
                    i -= 1  # Adjust for outer loop increment
            
            current_roles.append(role)
        
        i += 1
    
    # Process the last company
    if current_company and current_roles:
        if len(current_roles) == 1:
            role = current_roles[0]
            experiences.append({
                "company": current_company,
                "role": role["title"],
                "start_date": role["start_date"],
                "end_date": role["end_date"],
                "responsibilities": role["responsibilities"]
            })
        else:
            experiences.append({
                "company": current_company,
                "roles": current_roles
            })
    
    return experiences

def get_work_experience(config):
    md_path = Path(config['docs_dir'], "work-experience.md")

    if md_path.exists():
        content = md_path.read_text()
        content_parts = content.split('---')
        if len(content_parts) >= 3:
            content = content_parts[2]
        experiences = parse_markdown_content(content)
        return {"work_experience": experiences}
    return {md_path}

# For testing outside of MkDocs:
if __name__ == "__main__":
    test_config = WorkExperienceConfig()
    test_config['docs_dir'] = 'docs'  # Set to current directory for testing
    print(get_work_experience(test_config))
