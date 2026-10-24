# %% [code]
"""awesome_ui: Convenient df viz for notebooks."""
import uuid
import pandas as pd
from IPython.display import display, HTML

__all__ = ["display_fit_to_width"]

def _format_unit(val):
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
    max_height="350px"):
    
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
        .{container_class}-wrapper {{
            border: 1px solid #d1d5db;
            border-radius: 6px;
            margin-bottom: 16px;
            background-color: #ffffff;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            display: table;
            width: auto;
            max-width: 100%;
            box-sizing: border-box;
        }}
        .{container_class} {{
            max-height: {max_height} !important;
            overflow-y: auto !important;
            overflow-x: auto !important;
            width: 100% !important;
            box-sizing: border-box;
        }}
        /* Custom scrollbar styling */
        .{container_class}::-webkit-scrollbar {{
            height: 10px;
            width: 10px;
        }}
        .{container_class}::-webkit-scrollbar-track {{
            background: #f1f5f9;
            border-radius: 0 0 6px 6px;
        }}
        .{container_class}::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 5px;
        }}
        .{container_class}::-webkit-scrollbar-thumb:hover {{
            background: #94a3b8;
        }}
        .{container_class} table {{
            width: auto !important;
            min-width: 100% !important;
            table-layout: auto !important;
            border-collapse: collapse !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            font-size: 11px;
            margin: 0 !important;
        }}
        .{container_class} th, 
        .{container_class} td {{
            padding: 6px 10px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            border-bottom: 1px solid #e5e7eb;
            border-right: 1px solid #f3f4f6;
            text-align: left;
        }}
        {dynamic_css}
        .{container_class} table thead th {{
            position: sticky !important;
            top: 0 !important;
            z-index: 20 !important;
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            border-bottom: 2px solid #cbd5e1 !important;
        }}
    </style>
    
    <div class="{container_class}-wrapper">
        <div class="{container_class}">
            {df.to_html(classes="", index=True)}
        </div>
    </div>
    """
    display(HTML(html))