# Learning Notebooks

This directory contains Jupyter notebooks organized by learning phases, following the AutoGen + Modular Python learning journey.

## Structure

### Learning Phase Organization
```
notebooks/
├── 1-introduction/     # ✅ Basic concepts and first agent
├── 2-fundamentals/     # Core AutoGen features (upcoming)
├── 3-advanced/         # Complex patterns (upcoming)
├── 4-production/       # Real-world applications (upcoming)
├── playground/         # Free experimentation (upcoming)
└── shared/            # Notebook utilities and helpers
```

## Current Progress

### Phase 1: Introduction ✅
- [x] `first_agent.ipynb` - Your first AutoGen agent exploration

### Phase 2: Fundamentals (Coming Soon)
- [ ] `async_basics.ipynb` - Understanding async/await
- [ ] `agent_configuration.ipynb` - Agent setup and configuration
- [ ] `model_clients.ipynb` - Working with different model clients

### Phase 3: Advanced (Coming Soon)
- [ ] `multi_agent_teams.ipynb` - Team coordination
- [ ] `tool_integration.ipynb` - Custom tools and functions
- [ ] `advanced_patterns.ipynb` - Complex agent behaviors

### Phase 4: Production (Coming Soon)
- [ ] `testing_strategies.ipynb` - Testing async agent systems
- [ ] `deployment_patterns.ipynb` - Production deployment
- [ ] `monitoring_agents.ipynb` - Observability and monitoring

## Using Notebooks with Source Code

### Import Pattern
```python
# Add source code to path
import sys
sys.path.append('../src')

# Import from your modular source
from agents.base import BaseAgent
from config.settings import get_settings
```

### Shared Utilities
```python
# Import notebook utilities
from shared.notebook_utils import setup_environment, create_test_agent
```

## Best Practices

1. **Experiment First** - Use notebooks for exploration and learning
2. **Extract Patterns** - Move refined code to `src/` for reuse
3. **Document Insights** - Add markdown cells with your learnings
4. **Stay Organized** - Keep notebooks focused on specific topics
5. **Reference Clean Code** - Import from `src/` rather than duplicating

## Navigation Tips

- Each phase builds on the previous one
- Complete notebooks in order for best learning progression
- Use the shared utilities for common setup tasks
- Reference the main CLAUDE.md for overall learning roadmap

---

*This structure will evolve as you progress through your AutoGen learning journey!*