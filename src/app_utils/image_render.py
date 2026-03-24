import streamlit as st
import streamlit.components.v1 as components
import base64
from src.variables.partners import Partner
import os


class ImageRenderer:

    @staticmethod
    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    @staticmethod
    def tight_image(partner: Partner):
        image = partner.logo
        url = partner.url
        img_base64 = ImageRenderer.get_base64_image(image)
        extention = image.split('.')[-1]
        st.markdown("""
            <style>
            .bottom-align {
                display: flex;
                align-items: flex-end;
                height: 100%;
                padding: 0;
                margin: 0;
            }
            .tight-image {
                max-width: 100%;
                max-height: 100%;
                width: auto;
                height: auto;
                object-fit: contain;
                display: block;
                margin: 0;
                padding: 0;
            }
            </style>
            """, unsafe_allow_html=True)

        st.markdown('<div class="bottom-align">', unsafe_allow_html=True)

        st.markdown(f"""
            <a href="{url}" target="_blank">
                <img src="data:image/{extention};base64,{img_base64}" class="tight-image" alt="Logo">
            </a>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    @staticmethod
    def partner_banner_scroll_working(partners_list, logo_height=80):
        """Banner rendered via st.components.v1.html() to avoid Streamlit size limits
        and column div interference. Logos scale fluidly with viewport width."""

        logos_html = ""
        for partner in partners_list:
            img_base64 = ImageRenderer.get_base64_image(partner.logo)
            if img_base64:
                extension = partner.logo.split('.')[-1].lower()
                logos_html += f"""
                <div class="partner-logo-item">
                    <a href="{partner.url}" target="_blank">
                        <img src="data:image/{extension};base64,{img_base64}"
                             alt="{partner.name}" title="{partner.full_name}">
                    </a>
                </div>"""

        img_min = int(logo_height * 0.4)
        # vw value so logo reaches full height at ~1000px wide viewport
        img_vw = round(logo_height / 10, 1)

        # Calculate estimated number of rows based on number of logos
        # Assume roughly 4-6 logos per row depending on viewport
        estimated_logos_per_row = 5
        estimated_rows = max(1, (len(partners_list) + estimated_logos_per_row - 1) // estimated_logos_per_row)

        # iframe height: title (~50px) + estimated rows of logos + extra padding for safety
        iframe_height = logo_height * estimated_rows + 120

        html = f"""
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ background: transparent; }}
            .banner-title {{
                text-align: center;
                color: #333;
                margin-bottom: 20px;
                font-size: 1.1rem;
                font-weight: 600;
                font-family: sans-serif;
            }}
            .logo-row {{
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                justify-content: center;
                gap: clamp(10px, 2vw, 30px);
                padding: 10px;
            }}
            .partner-logo-item {{
                display: flex;
                align-items: center;
                justify-content: center;
                transition: transform 0.3s ease;
            }}
            .partner-logo-item:hover {{ transform: scale(1.05); }}
            .partner-logo-item img {{
                height: clamp({img_min}px, {img_vw}vw, {logo_height}px);
                width: auto;
                object-fit: contain;
            }}
        </style>
        <p class="banner-title">Partners</p>
        <div class="logo-row">
            {logos_html}
        </div>
        """

        components.html(html, height=iframe_height, scrolling=False)