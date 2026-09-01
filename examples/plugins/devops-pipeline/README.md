# DevOps Pipeline Plugin

CI/CD automation, deployment, and infrastructure management.

## Install

```bash
bash install.sh
```

## Components

- **devops-sre agent**: Infrastructure and deployment specialist
- **/ship command**: Full deployment workflow
- **GitHub Actions workflow**: Automated CI/CD in your repo

## Quick Start

```bash
# Deploy to production
/ship --env production

# Check deployment status
!git log --oneline -5

# Configure CI/CD
# Review .github/workflows/claude-code-review.yml
```

## Features

✓ Automated deployments
✓ Infrastructure validation
✓ Rollback support
✓ Health monitoring
✓ Alert integration

---

See `guide/ops/devops-sre.md` for full documentation.
