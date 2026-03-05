

class CSS:

    CONTAINER_3 = """
        {
            background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.1);
       
        }
        """

    #backdrop - filter: blur(15
    #px);
    WELCOME = f"""
    .st-key-welcome {CONTAINER_3}
    """

    LOCATION = f"""
    .st-key-location {CONTAINER_3}
    """

    SPATIAL_VARIABLES = f"""
    .st-key-spatial_variables {CONTAINER_3}
    """

    BENEFIT = f"""
    .st-key-benefits {CONTAINER_3}
    """

    COST = f"""
    .st-key-costs {CONTAINER_3}
    """

    ESS = f"""
    .st-key-ess {CONTAINER_3}
    """

    HIDE_ANCHOR_CSS = """
    <style>
    /* Hide all possible anchor link elements */
    .stMarkdown h1 a,
    .stMarkdown h2 a,
    .stMarkdown h3 a,
    .stMarkdown h4 a,
    .stMarkdown h5 a,
    .stMarkdown h6 a {
        display: none !important;
    }

    /* Hide header action elements */
    .stHeaderActionElements {
        display: none !important;
    }

    /* Hide anchor icons specifically */
    .stMarkdown h1 .anchor,
    .stMarkdown h2 .anchor,
    .stMarkdown h3 .anchor {
        display: none !important;
    }

    /* More aggressive approach - hide any link-like elements in headers */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important;
    }

    /* Target data-testid elements that might contain anchors */
    [data-testid="stMarkdownContainer"] h1 a,
    [data-testid="stMarkdownContainer"] h2 a,
    [data-testid="stMarkdownContainer"] h3 a {
        display: none !important;
    }
    </style>
    """

    GOOGLE_FONT = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
    
    """

    TAB_LAYOUT = """
                <style>
                    /* Main container for tabs */
                    .stTabs [data-baseweb="tab-list"] {
                        gap: 2px;
                    }

                    /* Individual tab appearance */
                    .stTabs [data-baseweb="tab"] {
                        height: 50px;
                        white-space: pre-wrap;
                        background-color: #F0F2F6; /* Background for inactive tabs */
                        border-radius: 8px 8px 0px 0px; /* Rounded top corners */
                        gap: 1px;
                        padding-top: 3px;
                        padding-bottom: 3px;
                        padding-left: 20px;
                        padding-right: 20px;
                        border: 1px solid #ddd; /* Add a border to all tabs */
                        border-bottom: none; /* Remove bottom border for tab itself */
                    }

                    /* Active (selected) tab appearance */
                    .stTabs [aria-selected="true"] {
                        background-color: #FFFFFF; /* White background for active tab */
                        border-bottom: none; /* Ensure no bottom border to blend with content frame */
                    }

                </style>
                """
    LOADING_SCREEN = """
<style>
#loading-screen {
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background: #f8f9fa;
    z-index: 99999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: sans-serif;
}
.loading-spinner {
    width: 52px; height: 52px;
    border: 5px solid #e0e0e0;
    border-top-color: #006d77;
    border-radius: 50%;
    animation: spin 0.9s linear infinite;
    margin-bottom: 20px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.loading-text { color: #555; font-size: 1.1rem; font-weight: 500; }
</style>
<div id="loading-screen">
    <div class="loading-spinner"></div>
    <p class="loading-text">Loading…</p>
</div>
"""

    BIOME_SELECTION_BOX = """
        <style>
        .biome-box {
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: #f8f9fa;
            transition: all 0.3s ease;
            cursor: pointer;
            height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .biome-box:hover {
            border-color: #1f77b4;
            background-color: #e8f4fd;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .biome-box.selected {
            border-color: #1f77b4;
            background-color: #e8f4fd;
            border-width: 3px;
        }

        .biome-logo {
            font-size: 48px;
            margin-bottom: 10px;
        }

        .biome-name {
            font-size: 16px;
            font-weight: bold;
            color: #333;
            margin: 0;
        }
        </style>
        """

