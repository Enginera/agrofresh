import streamlit as st

def apply_custom_styles():
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-main: #F4F7F4;
        --surface: #FFFFFF;
        --surface-glass: rgba(255, 255, 255, 0.85);
        --brand-dark: #0A2518;
        --brand-forest: #1B4332;
        --brand-primary: #2D6A4F;
        --brand-sage: #52B788;
        --brand-lime: #74C69D;
        --accent-sand: #EFEFE9;
        --accent-terracotta: #D95D39;
        --text-primary: #121F17;
        --text-secondary: #586B60;
        --border-subtle: #DDE5DF;
        --border-focus: #52B788;
        --shadow-sm: 0 2px 8px rgba(10, 37, 24, 0.04);
        --shadow-md: 0 8px 24px rgba(10, 37, 24, 0.07);
        --radius-sm: 8px;
        --radius-md: 14px;
        --radius-lg: 20px;
    }

    /* Global typography */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
    }

    /* Hero Header */
    .hero-banner {
        background: linear-gradient(135deg, #0A2518 0%, #1B4332 50%, #2D6A4F 100%);
        border-radius: var(--radius-lg);
        padding: 32px 36px;
        color: #FFFFFF !important;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(116, 198, 157, 0.2) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        color: #B7E4C7;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        padding: 5px 12px;
        border-radius: 30px;
        margin-bottom: 12px;
        border: 1px solid rgba(255, 255, 255, 0.12);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        margin: 0 0 8px 0;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: #D8F3DC;
        font-weight: 400;
        max-width: 750px;
        margin: 0;
        line-height: 1.5;
    }

    /* Metric Cards */
    .metric-grid-card {
        background: var(--surface);
        border-radius: var(--radius-md);
        padding: 22px 20px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-sm);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .metric-grid-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
        border-color: var(--brand-sage);
    }
    .metric-grid-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--brand-primary), var(--brand-sage));
    }
    .metric-label-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .metric-icon-badge {
        font-size: 1.1rem;
        background: var(--bg-main);
        padding: 6px;
        border-radius: 8px;
        line-height: 1;
    }
    .metric-value-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 700;
        color: var(--brand-dark);
        letter-spacing: -0.8px;
        line-height: 1.1;
    }
    .metric-unit {
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--text-secondary);
        font-family: 'Plus Jakarta Sans', sans-serif;
        margin-left: 4px;
    }
    .metric-pill {
        margin-top: 10px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 12px;
    }
    .pill-green {
        background-color: #E8F5E9;
        color: #1B5E20;
    }
    .pill-orange {
        background-color: #FBE9E7;
        color: #D84315;
    }

    /* Calculator Box */
    .calc-container {
        background: linear-gradient(145deg, #FFFFFF 0%, #F9FAF8 100%);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        padding: 28px;
        box-shadow: var(--shadow-sm);
        margin-top: 24px;
        margin-bottom: 24px;
    }
    .calc-header {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--brand-dark);
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .calc-desc {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 20px;
    }
    .calc-result-card {
        background: #FFFFFF;
        border-radius: var(--radius-md);
        padding: 20px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-sm);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .calc-result-card.accent-emerald {
        background: linear-gradient(145deg, #F0FDF4 0%, #E8F7ED 100%);
        border: 1px solid #A7F3D0;
    }
    .calc-result-card.accent-blue {
        background: linear-gradient(145deg, #F0FDFB 0%, #E6F8F6 100%);
        border: 1px solid #99F6E4;
    }
    .calc-res-title {
        font-size: 0.8rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.7px;
        color: var(--text-secondary);
        margin-bottom: 4px;
    }
    .calc-res-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.65rem;
        font-weight: 700;
        color: var(--brand-dark);
        margin-top: 4px;
    }

    /* Reference & Formula Cards */
    .formula-card {
        background: #FFFFFF;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-subtle);
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: var(--shadow-sm);
    }
    .formula-card h3 {
        color: var(--brand-forest);
        font-size: 1.15rem;
        font-weight: 700;
        margin-top: 0;
        margin-bottom: 14px;
    }
    .data-table-badge {
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        background: #EDF5F0;
        color: #1B4332;
        padding: 2px 7px;
        border-radius: 6px;
        border: 1px solid #D4E8DC;
    }

    /* Sidebar Refinement */
    [data-testid="stSidebar"] {
        background-color: #FAFBF9 !important;
        border-right: 1px solid var(--border-subtle) !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: var(--border-subtle) !important;
    }

    /* Plotly container clean */
    .stPlotlyChart {
        background: #FFFFFF;
        border-radius: var(--radius-md);
        border: 1px solid var(--border-subtle);
        padding: 8px;
        box-shadow: var(--shadow-sm);
    }

    /* Streamlit overrides */
    div[data-testid="stExpander"] {
        border: 1px solid var(--border-subtle) !important;
        border-radius: var(--radius-md) !important;
        background: #FFFFFF !important;
        box-shadow: var(--shadow-sm) !important;
    }
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)