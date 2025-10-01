# Contributing to Fabric Agentic Workloads Lab

Thank you for your interest in contributing! This lab is a community-driven project, and we welcome contributions of all kinds.

## 🤝 How to Contribute

### Types of Contributions We Welcome

1. **New Exercises and Examples**
   - Additional agent patterns
   - Industry-specific use cases
   - Advanced scenarios
   - Integration examples

2. **Documentation Improvements**
   - Clarify existing instructions
   - Add troubleshooting tips
   - Translate content
   - Fix typos and errors

3. **Code Enhancements**
   - Bug fixes
   - Performance improvements
   - New features
   - Test coverage

4. **Sample Data and Scripts**
   - Additional datasets
   - Helper utilities
   - Testing frameworks
   - Deployment scripts

## 🚀 Getting Started

### 1. Fork the Repository
```bash
# Click "Fork" on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/Fabric.git
cd Fabric
```

### 2. Create a Branch
```bash
# Create a descriptive branch name
git checkout -b feature/add-financial-agent-example
# or
git checkout -b fix/module8-typo
```

### 3. Make Your Changes

Follow our coding standards:

#### Python Code Style
- Use PEP 8 guidelines
- Add docstrings to functions and classes
- Include type hints where appropriate
- Keep functions focused and small

Example:
```python
def process_data(input: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process input data according to configuration.
    
    Args:
        input: The input data to process
        config: Configuration dictionary with processing parameters
        
    Returns:
        Dictionary containing processed results
        
    Raises:
        ValueError: If input is invalid
    """
    # Implementation here
    pass
```

#### Documentation Style
- Use clear, concise language
- Include code examples where helpful
- Add diagrams for complex concepts
- Structure with headings and lists

#### Markdown Format
```markdown
# Main Title

## Section

### Subsection

- Bullet points for lists
- Use **bold** for emphasis
- Use `code` for inline code
- Use ```python for code blocks
```

### 4. Test Your Changes

Before submitting:
```bash
# Run your code
python your_script.py

# Check for syntax errors
python -m py_compile your_script.py

# If you added tests
pytest tests/
```

### 5. Commit Your Changes
```bash
# Add your changes
git add .

# Commit with a descriptive message
git commit -m "Add financial services agent example with fraud detection"

# Push to your fork
git push origin feature/add-financial-agent-example
```

### 6. Submit a Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request"
3. Select your branch
4. Fill in the PR template:
   - **Title**: Clear, descriptive title
   - **Description**: What changes you made and why
   - **Testing**: How you tested the changes
   - **Screenshots**: If applicable

## 📋 Contribution Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Welcome newcomers
- Focus on the content, not the person

### Quality Standards

#### For Code:
- ✅ Works as described
- ✅ Includes error handling
- ✅ Has helpful comments
- ✅ Follows existing patterns
- ✅ No hardcoded credentials

#### For Documentation:
- ✅ Clear and concise
- ✅ Accurate and tested
- ✅ Well-structured
- ✅ Free of typos
- ✅ Includes examples

#### For Examples:
- ✅ Demonstrates one concept clearly
- ✅ Includes explanatory comments
- ✅ Uses sample data (no real data)
- ✅ Has clear expected output
- ✅ Can run independently

### What We DON'T Accept

- ❌ Copyrighted material without permission
- ❌ Real credentials or sensitive data
- ❌ Malicious code
- ❌ Unrelated or off-topic content
- ❌ Breaking existing functionality without reason

## 🐛 Reporting Bugs

Found a bug? Please report it!

### How to Report:
1. Check [existing issues](https://github.com/ralphke/Fabric/issues)
2. If not found, create a new issue
3. Include:
   - **Description**: What's wrong?
   - **Steps to Reproduce**: How can we see the bug?
   - **Expected Behavior**: What should happen?
   - **Actual Behavior**: What actually happens?
   - **Environment**: OS, Python version, etc.
   - **Screenshots**: If applicable

### Example Bug Report:
```markdown
**Description**: Exercise 2 agent throws error when using GPT-4

**Steps to Reproduce**:
1. Set AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4 in .env
2. Run python exercise2_tool_agent.py
3. Error occurs on line 45

**Expected**: Agent completes task successfully

**Actual**: KeyError: 'function_call'

**Environment**:
- OS: Windows 11
- Python: 3.11.5
- openai package: 1.12.0
```

## 💡 Suggesting Enhancements

Have an idea? We'd love to hear it!

### How to Suggest:
1. Check [existing issues](https://github.com/ralphke/Fabric/issues)
2. Create a new issue with "Enhancement" label
3. Describe:
   - **Feature**: What do you want to add?
   - **Motivation**: Why is this useful?
   - **Examples**: How would it work?
   - **Alternatives**: Other options considered?

## 📚 Documentation Contributions

### Priority Areas:
- Troubleshooting guides
- Video tutorials
- Translations
- Architecture diagrams
- Real-world case studies

### Style Guide:
- Use active voice
- Keep sentences short
- Define acronyms on first use
- Include practical examples
- Link to official documentation

## 🎯 Good First Issues

New to contributing? Look for issues labeled:
- `good first issue`
- `documentation`
- `help wanted`

These are great starting points!

## 🔍 Review Process

After you submit a PR:

1. **Automated Checks**: GitHub Actions run
2. **Maintainer Review**: We'll review your code
3. **Feedback**: We may suggest changes
4. **Approval**: Once ready, we'll merge!

Response time: Usually within 3-5 days

## 🙏 Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

## 📞 Questions?

- **General**: [GitHub Discussions](https://github.com/ralphke/Fabric/discussions)
- **Contribution Help**: Create an issue with "question" label
- **Private Matters**: Contact maintainers directly

## 📄 License

By contributing, you agree that your contributions will be licensed under the GPL-3.0 License.

---

**Thank you for making this lab better for everyone!** 🎉
