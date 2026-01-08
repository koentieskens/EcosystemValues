

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

