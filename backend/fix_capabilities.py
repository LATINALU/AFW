#!/usr/bin/env python3
"""Fix invalid AgentCapability values in all agent files"""
import os
import re

# Mapping of invalid capabilities to valid ones
CAPABILITY_FIXES = {
    "AgentCapability.CONTENT": "AgentCapability.WRITING",
    "AgentCapability.CREATIVITY": "AgentCapability.CREATIVE",
    "AgentCapability.NEGOTIATION": "AgentCapability.COMMUNICATION",
    "AgentCapability.STRATEGY": "AgentCapability.PLANNING",
    "AgentCapability.ARCHITECTURE": "AgentCapability.SYSTEM_ARCHITECTURE",
    "AgentCapability.DESIGN": "AgentCapability.CREATIVE",
    "AgentCapability.PEDAGOGY": "AgentCapability.EDUCATIONAL",
    "AgentCapability.ASSESSMENT": "AgentCapability.VALIDATION",
    "AgentCapability.TALENT": "AgentCapability.COORDINATION",
    "AgentCapability.HR": "AgentCapability.COORDINATION",
    "AgentCapability.ACCOUNTING": "AgentCapability.FINANCIAL",
    "AgentCapability.SALES": "AgentCapability.MARKETING",
    "AgentCapability.BRANDING": "AgentCapability.CREATIVE",
    "AgentCapability.ANIMATION": "AgentCapability.CREATIVE",
    "AgentCapability.VIDEO": "AgentCapability.CREATIVE",
    "AgentCapability.UI": "AgentCapability.CREATIVE",
    "AgentCapability.UX": "AgentCapability.CREATIVE",
    "AgentCapability.LEADERSHIP": "AgentCapability.COORDINATION",
    "AgentCapability.FACILITATION": "AgentCapability.COORDINATION",
    "AgentCapability.PROCUREMENT": "AgentCapability.COORDINATION",
    "AgentCapability.LOGISTICS": "AgentCapability.COORDINATION",
    "AgentCapability.QUALITY": "AgentCapability.QA",
    "AgentCapability.BUDGETING": "AgentCapability.FINANCIAL",
    "AgentCapability.TRAINING": "AgentCapability.EDUCATIONAL",
    "AgentCapability.EVALUATION": "AgentCapability.VALIDATION",
    # Round 2 fixes
    "AgentCapability.CREATIVE_UX": "AgentCapability.CREATIVE",
    "AgentCapability.DEVOPS": "AgentCapability.TECHNICAL",
    "AgentCapability.DECISION": "AgentCapability.DECISION_MAKING",
    "AgentCapability.AUTOMATION": "AgentCapability.TECHNICAL",
    "AgentCapability.INNOVATION": "AgentCapability.CREATIVE",
    "AgentCapability.OPERATIONS": "AgentCapability.COORDINATION",
    "AgentCapability.COACHING": "AgentCapability.EDUCATIONAL",
    "AgentCapability.EDUCATION": "AgentCapability.EDUCATIONAL",
    "AgentCapability.RELATIONSHIP": "AgentCapability.COMMUNICATION",
    "AgentCapability.SUPPORT": "AgentCapability.COMMUNICATION",
    # Round 3 fixes
    "AgentCapability.MENTORING": "AgentCapability.EDUCATIONAL",
    "AgentCapability.PRODUCTION": "AgentCapability.CREATIVE",
    "AgentCapability.STORYTELLING": "AgentCapability.CREATIVE",
    "AgentCapability.ART": "AgentCapability.CREATIVE",
    "AgentCapability.PROJECT_MANAGEMENT": "AgentCapability.COORDINATION",
    "AgentCapability.PRODUCT": "AgentCapability.PLANNING",
    "AgentCapability.CHANGE": "AgentCapability.COORDINATION",
    "AgentCapability.INFLUENCE": "AgentCapability.COMMUNICATION",
    "AgentCapability.ORGANIZATION": "AgentCapability.COORDINATION",
    "AgentCapability.BUSINESS": "AgentCapability.FINANCIAL",
    "AgentCapability.GOVERNANCE": "AgentCapability.COORDINATION",
    # Fix double replacements
    "AgentCapability.EDUCATIONALAL": "AgentCapability.EDUCATIONAL",
    "AgentCapability.DECISION_MAKING_MAKING": "AgentCapability.DECISION_MAKING",
}

def fix_file(filepath):
    """Fix capabilities in a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for old, new in CAPABILITY_FIXES.items():
            content = content.replace(old, new)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error fixing {filepath}: {e}")
        return False

def main():
    agents_dir = "/app/app/agents"
    fixed_count = 0
    
    for root, dirs, files in os.walk(agents_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if fix_file(filepath):
                    print(f"✅ Fixed: {filepath}")
                    fixed_count += 1
    
    print(f"\n🔧 Total files fixed: {fixed_count}")

if __name__ == "__main__":
    main()
