# awesome_ui
⚙️ Executive-grade UI utilities for notebooks

`awesome_ui` provides standardized, cross-browser table rendering that solves iframe CSS leaks, fixes sticky header clipping, and gives you pixel-perfect column width control across notebooks.

## Key Features

- **Isolated CSS Scoping:** Generates unique DOM instances via UUIDs to prevent style collisions when rendering multiple tables in a single notebook cell.
- **Responsive Flex Layout:** Uses `table-layout: fixed` and CSS `calc()` for mathematically balanced, non-overflowing column widths.
- **Smart Sizing Units:** Automatically distinguishes pixel allocations (`px`) for index columns and percentages (`%`) for data features.
- **Index Control:** Hide, narrow, or expand DataFrame index columns with zero layout distortion.

## Quickstart

```python
import pandas as pd
from awesome_ui import display_fit_to_width

# Standard auto-fitted display (responsive equal distribution)
display_fit_to_width(df)

# Hide index completely
display_fit_to_width(df, index_width=0)

# Granular column width overrides (Index 1 = df index)
display_fit_to_width(
    df, 
    col_widths={1: 5, 2: "30%", 3: 15, 4: 15, 5: 10, 6: 10, 7: 15}
)
```

