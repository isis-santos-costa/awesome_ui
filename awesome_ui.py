"""
awesome_ui: Executive-grade UI utilities for notebooks.
"""
import uuid
import pandas as pd
from IPython.display import display, HTML

__all__ = ["display_fit_to_width"]


def _format_unit(val):
    """Sanitizes raw numbers into explicit CSS units (px vs %)."""
    if val is None:
        return "0px"
    val_str = str(val).strip()
    if val_str.isdigit():
        return f"{val_str}px"
    return val_str


def display_fit_to_width(
    df, 
    index_width="35px", 
    col_widths=None, 
    max_height="350px"
):
    """
    Renders a pandas DataFrame in a full-width, scrollable HTML container.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to display.
        
    index_width : str or int, default "35px"
        Explicit width for Column 1 (Index). 
        Set to 0, "0", "0px", or None to completely omit/hide the index.
        
    col_widths : dict, optional
        1-based column index mapped to its % width (index 1 = df index).
        Example: {2: "35%", 3: "15%"} OR {2: 35, 3: 15}
        If omitted, width is divided equally across data columns.
        
    max_height : str, default "350px"
        Max vertical viewport height before scrolling triggers.
    """
    unique_id = uuid.uuid4().hex[:8]
    container_class = f"fit-to-width-container-{unique_id}"

    formatted_index_width = _format_unit(index_width)
    hide_index = formatted_index_width in ("0px", "0%", "0")
    
    num_data_cols = len(df.columns)
    
    final_widths = {}
    
    if hide_index:
        final_widths[1] = "HIDE"
    else:
        final_widths[1] = formatted_index_width
        
    if col_widths is None:
        if num_data_cols > 0:
            if hide_index:
                equal_width_str = f"{100 / num_data_cols:.2f}%"
            else:
                equal_width_str = f"calc((100% - {formatted_index_width}) / {num_data_cols})"
                
            for idx in range(2, num_data_cols + 2):
                final_widths[idx] = equal_width_str
    else:
        for idx, w in col_widths.items():
            final_widths[idx] = _format_unit(w)

    custom_col_styles = []
    for col_idx, width_str in final_widths.items():
        if width_str == "HIDE":
            css_block = f"""
            .{container_class} th:nth-child(1),
            .{container_class} td:nth-child(1) {{
                display: none !important;
            }}
            """
        else:
            css_block = f"""
            .{container_class} th:nth-child({col_idx}),
            .{container_class} td:nth-child({col_idx}) {{
                width: {width_str} !important;
                min-width: {width_str} !important;
                max-width: {width_str} !important;
            }}
            """
        custom_col_styles.append(css_block)
    
    dynamic_css = "\n".join(custom_col_styles)

    html = f"""
    <style>
        .{container_class} {{
            max-height: {max_height} !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
            width: 100% !important;
            border: 1px solid #d1d5db;
            border-radius: 4px;
            margin-bottom: 16px;
            box-sizing: border-box;
            background-color: #ffffff;
        }}
        
        .{container_class} table {{
            width: 100% !important;
            table-layout: fixed !important;
            border-collapse: collapse !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 11px;
            margin: 0 !important;
        }}
        
        .{container_class} th, 
        .{container_class} td {{
            padding: 6px 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            border-bottom: 1px solid #e5e7eb;
            border-right: 1px solid #f3f4f6;
            text-align: left;
        }}

        /* Apply Instance Column Styles */
        {dynamic_css}

        .{container_class} table thead th {{
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            border-bottom: 2px solid #cbd5e1 !important;
        }}
    </style>
    
    <div class="{container_class}">
        {df.to_html(classes="", index=True)}
    </div>
    """
    display(HTML(html))
