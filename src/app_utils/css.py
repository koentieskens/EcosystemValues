

class CSS:

    CONTAINER_3 = """
    {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 24px 28px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.2s ease;
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

    PARTNERS = f"""
    .st-key-partners {CONTAINER_3}
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

    WORLD_BANK_STYLE_FONT = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600&display=swap');

            html, body, [class*="css"] {
                font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
                font-weight: 400;
            }

            /* Professional typography hierarchy */
            h1, h2, h3 {
                font-weight: 600;
                color: #002345;
            }

            .light-text {
                font-weight: 300;
            }

            /* Section header accent bar (main content h2 only) */
            [data-testid="stMain"] h2 {
                border-left: 4px solid #006C99;
                padding-left: 12px;
            }

            /* Sidebar subheader styling */
            [data-testid="stSidebar"] h3 {
                font-size: 0.78rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                color: #6b7280;
                margin-bottom: 8px;
            }

            /* Sidebar divider */
            [data-testid="stSidebar"] hr {
                border: none;
                border-top: 1px solid #e5e7eb;
                margin: 12px 0;
            }
        </style>
        """

    TAB_LAYOUT = """
                    <style>
                        /* Main container for tabs */
                        .stTabs [data-baseweb="tab-list"] {
                            gap: 0px;
                            border-bottom: 1px solid #e5e7eb;
                        }

                        /* Individual tab appearance */
                        .stTabs [data-baseweb="tab"] {
                            height: 48px;
                            white-space: pre-wrap;
                            background-color: #f8f9fa;
                            border-radius: 6px 6px 0px 0px;
                            gap: 1px;
                            padding-top: 12px;
                            padding-bottom: 12px;
                            padding-left: 24px;
                            padding-right: 24px;
                            border: 1px solid #e5e7eb;
                            border-bottom: 1px solid #e5e7eb;
                            color: #6b7280;
                            font-weight: 400;
                            transition: all 0.2s ease;
                            margin-bottom: -1px;
                        }

                        /* Hover state for inactive tabs */
                        .stTabs [data-baseweb="tab"]:hover {
                            background-color: #f3f4f6;
                            color: #374151;
                        }

                        /* Active (selected) tab appearance */
                        .stTabs [aria-selected="true"] {
                            background-color: #ffffff;
                            border: 1px solid #e5e7eb;
                            border-bottom: 1px solid #ffffff;
                            color: #002345;
                            font-weight: 500;
                            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                        }

                        /* Tab content area styling - NO BORDER */
                        .stTabs [data-baseweb="tab-panel"] {
                            background-color: #ffffff;
                            border: none;
                            border-radius: 0px;
                            padding: 0px;
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
                border: 1px solid #e5e7eb;
                border-radius: 6px;
                padding: 24px;
                text-align: center;
                background-color: #ffffff;
                transition: all 0.2s ease;
                cursor: pointer;
                height: 150px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            }

            .biome-box:hover {
                border-color: #002345;
                background-color: #f8f9fa;
                box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.1);
            }

            .biome-box.selected {
                border-color: #002345;
                background-color: #f8f9fa;
                border-width: 2px;
                box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08), 0 1px 3px rgba(0, 0, 0, 0.1);
            }

            .biome-logo {
                font-size: 48px;
                margin-bottom: 12px;
                opacity: 0.8;
                transition: opacity 0.2s ease;
            }

            .biome-box:hover .biome-logo,
            .biome-box.selected .biome-logo {
                opacity: 1;
            }

            .biome-name {
                font-size: 16px;
                font-weight: 500;
                color: #002345;
                margin: 0;
                font-family: 'Source Sans Pro', 'Helvetica Neue', Arial, sans-serif;
            }
            </style>
            """

