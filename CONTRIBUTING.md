# Contributing to XploitRecon

First off, thank you for considering contributing to XploitRecon! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)

## 📜 Code of Conduct

This project and everyone participating in it is governed by common sense and respect. By participating, you are expected to uphold this standard.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and expected**
- **Include screenshots if applicable**
- **Include your environment details** (OS, Python version, tool versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List examples of how it would be used**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Test your changes thoroughly
4. Update documentation if needed
5. Create a Pull Request

## 🛠️ Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/XploitRecon.git
cd XploitRecon

# Install dependencies
bash install.sh

# Create a new branch
git checkout -b feature/your-feature-name
```

## 🔄 Pull Request Process

1. **Update the README.md** with details of changes if applicable
2. **Update the version number** in relevant files
3. **Ensure all tests pass** (if applicable)
4. **Follow the coding standards** outlined below
5. **Write clear commit messages**

### Commit Message Format

```
type: subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

Example:
```
feat: add progress bar for nuclei scanning

Added a real-time progress bar to show scan progress
during nuclei vulnerability scanning phase.

Closes #123
```

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions and classes

### Code Organization

```python
#!/usr/bin/env python3
"""
Module description
"""

# Standard library imports
import os
import sys

# Third-party imports
import requests

# Local imports
from .utils import helper_function

# Constants
CONSTANT_NAME = "value"

# Classes
class ClassName:
    """Class description"""
    pass

# Functions
def function_name(param):
    """Function description"""
    pass
```

### Documentation

- Add docstrings to all functions and classes
- Update README.md for new features
- Add code comments for complex logic
- Include usage examples

## 🧪 Testing

Before submitting a PR, please test your changes:

```bash
# Test basic functionality
./xploitrecon.py -d example.com -s critical

# Test error handling
./xploitrecon.py -d invalid_domain

# Test different severity levels
./xploitrecon.py -d example.com -s critical,high,medium
```

## 💡 Feature Ideas

Looking for ideas? Here are some features we'd love to see:

- [ ] Progress bar for Nuclei scanning
- [ ] Multi-domain scanning support
- [ ] Discord/Telegram notifications
- [ ] HTML/PDF report generation
- [ ] Database support for scan history
- [ ] Resume interrupted scans
- [ ] Custom wordlist support
- [ ] Rate limiting configuration
- [ ] Proxy support
- [ ] API endpoint

## 📞 Getting Help

If you need help, you can:

- Open an issue with the `question` label
- Check existing issues and discussions
- Review the documentation

## 🙏 Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute!

---

**Happy Coding! 🚀**

*- CtoXpLt_*
