import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import database as db

def apply_custom_theme(theme="dark"):
    """Apply custom CSS theme"""
    
    if theme == "dark":
        bg_color = "#1a1a2e"
        accent_color = "#00d4ff"
        text_color = "#ffffff"
        card_bg = "#16213e"
    else:
        bg_color = "#ffffff"
        accent_color = "#0066cc"
        text_color = "#000000"
        card_bg = "#f0f2f6"
    
    st.markdown(f"""
    <style>
        /* Main container */
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        
        /* Sidebar */
        .css-1d391kg, .css-1wrcr25 {{
            background-color: {card_bg};
        }}
        
        /* Custom auth form styling */
        .auth-wrapper {{
            position: relative;
            width: 100%;
            max-width: 800px;
            height: 500px;
            margin: 0 auto;
            border: 2px solid {accent_color};
            box-shadow: 0 0 25px {accent_color};
            overflow: hidden;
            background: {bg_color};
        }}
        
        .auth-wrapper .credentials-panel {{
            position: absolute;
            top: 0;
            width: 50%;
            height: 100%;
            display: flex;
            justify-content: center;
            flex-direction: column;
        }}
        
        .credentials-panel.signin {{
            left: 0;
            padding: 0 40px;
        }}
        
        .credentials-panel.signup {{
            right: 0;
            padding: 0 60px;
        }}
        
        .credentials-panel h2 {{
            font-size: 32px;
            text-align: center;
            color: {text_color};
        }}
        
        .field-wrapper {{
            position: relative;
            width: 100%;
            height: 50px;
            margin-top: 25px;
        }}
        
        .field-wrapper input {{
            width: 100%;
            height: 100%;
            background: transparent;
            border: none;
            outline: none;
            font-size: 16px;
            color: {text_color};
            font-weight: 600;
            border-bottom: 2px solid {text_color};
            padding-right: 23px;
            transition: .5s;
        }}
        
        .field-wrapper input:focus,
        .field-wrapper input:valid {{
            border-bottom: 2px solid {accent_color};
        }}
        
        .field-wrapper label {{
            position: absolute;
            top: 50%;
            left: 0;
            transform: translateY(-50%);
            font-size: 16px;
            color: {text_color};
            transition: .5s;
        }}
        
        .field-wrapper input:focus ~ label,
        .field-wrapper input:valid ~ label {{
            top: -5px;
            color: {accent_color};
        }}
        
        .field-wrapper i {{
            position: absolute;
            top: 50%;
            right: 0;
            font-size: 18px;
            transform: translateY(-50%);
            color: {text_color};
        }}
        
        .field-wrapper input:focus ~ i,
        .field-wrapper input:valid ~ i {{
            color: {accent_color};
        }}
        
        .submit-button {{
            position: relative;
            width: 100%;
            height: 45px;
            background: transparent;
            border-radius: 40px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            color: {text_color};
            border: 2px solid {accent_color};
            overflow: hidden;
            z-index: 1;
            transition: .5s;
        }}
        
        .submit-button:hover {{
            color: {bg_color};
            background: {accent_color};
        }}
        
        .switch-link {{
            font-size: 14px;
            text-align: center;
            margin: 20px 0 10px;
            color: {text_color};
        }}
        
        .switch-link a {{
            text-decoration: none;
            color: {accent_color};
            font-weight: 600;
        }}
        
        .welcome-section {{
            position: absolute;
            top: 0;
            height: 100%;
            width: 50%;
            display: flex;
            justify-content: center;
            flex-direction: column;
        }}
        
        .welcome-section.signin {{
            right: 0;
            text-align: right;
            padding: 0 40px 60px 150px;
        }}
        
        .welcome-section.signup {{
            left: 0;
            text-align: left;
            padding: 0 150px 60px 38px;
        }}
        
        .welcome-section h2 {{
            text-transform: uppercase;
            font-size: 36px;
            line-height: 1.3;
            color: {text_color};
        }}
        
        .background-shape {{
            position: absolute;
            right: 0;
            top: -5px;
            height: 600px;
            width: 850px;
            background: linear-gradient(45deg, {bg_color}, {accent_color});
            transform: rotate(10deg) skewY(40deg);
            transform-origin: bottom right;
            transition: 1.5s ease;
        }}
        
        .secondary-shape {{
            position: absolute;
            left: 250px;
            top: 100%;
            height: 700px;
            width: 850px;
            background: {bg_color};
            border-top: 3px solid {accent_color};
            transform: rotate(0deg) skewY(0deg);
            transform-origin: bottom left;
            transition: 1.5s ease;
        }}
        
        .auth-wrapper.toggled .background-shape {{
            transform: rotate(0deg) skewY(0deg);
        }}
        
        .auth-wrapper.toggled .secondary-shape {{
            transform: rotate(-11deg) skewY(-41deg);
        }}
        
        /* Footer styling */
        .footer {{
            margin-top: 30px;
            text-align: center;
            padding: 15px;
            font-size: 14px;
            color: {text_color};
        }}
        
        .footer a {{
            color: {accent_color};
            text-decoration: none;
            font-weight: 600;
            margin: 0 10px;
            transition: .3s;
        }}
        
        .footer a:hover {{
            text-decoration: underline;
        }}
        
        /* Social icons */
        .social-icons {{
            margin-top: 10px;
        }}
        
        .social-icons a {{
            font-size: 20px;
            margin: 0 10px;
            color: {accent_color};
            text-decoration: none;
        }}
        
        /* Custom gauge styling */
        .gauge-container {{
            background: {card_bg};
            padding: 20px;
            border-radius: 10px;
            border: 1px solid {accent_color};
            margin: 10px 0;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .auth-wrapper {{
                height: auto;
                min-height: 500px;
            }}
            
            .auth-wrapper .credentials-panel,
            .welcome-section {{
                width: 100%;
                position: relative;
            }}
            
            .credentials-panel.signin,
            .credentials-panel.signup {{
                padding: 40px 30px;
                left: 0;
                right: 0;
            }}
            
            .welcome-section {{
                display: none;
            }}
            
            .background-shape,
            .secondary-shape {{
                display: none;
            }}
        }}
        
        /* Chat message styling */
        .user-message {{
            background: {accent_color}20;
            padding: 10px 15px;
            border-radius: 15px 15px 0 15px;
            margin: 5px 0;
            text-align: right;
            border: 1px solid {accent_color};
        }}
        
        .assistant-message {{
            background: {card_bg};
            padding: 10px 15px;
            border-radius: 15px 15px 15px 0;
            margin: 5px 0;
            border: 1px solid {accent_color}40;
        }}
        
        /* Progress heatmap styling */
        .heatmap-title {{
            color: {accent_color};
            font-size: 20px;
            font-weight: 600;
            margin: 20px 0 10px;
        }}
    </style>
    
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """, unsafe_allow_html=True)

def create_doubt_gauge(score):
    """Create a gauge chart for doubt score"""
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Doubt Score", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "#00d4ff"},
            'steps': [
                {'range': [0, 30], 'color': "#00ff0040"},
                {'range': [30, 70], 'color': "#ffff0040"},
                {'range': [70, 100], 'color': "#ff000040"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Poppins"}
    )
    
    return fig

def create_mastery_heatmap(user_id):
    """Create a heatmap of topic mastery"""
    
    progress_data = db.get_user_progress(user_id)
    
    if not progress_data:
        return None
    
    # Create DataFrame
    df = pd.DataFrame(progress_data, columns=['Topic', 'Mastery', 'Interactions', 'Last Studied'])
    
    # Create heatmap
    fig = px.imshow(
        [df['Mastery'].values],
        x=df['Topic'].values,
        y=['Mastery Level'],
        color_continuous_scale=['red', 'yellow', 'green'],
        aspect="auto",
        title="Topic Mastery Heatmap"
    )
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Poppins"},
        height=200
    )
    
    return fig

def render_sidebar():
    """Render the navigation sidebar"""
    
    with st.sidebar:
        # User greeting with custom styling
        st.markdown(f"""
        <div style='text-align: center; padding: 10px;'>
            <div style='font-size: 50px;'>🎓</div>
            <h3 style='color: #00d4ff; margin: 0;'>Welcome,</h3>
            <p style='color: #ffffff; font-size: 18px; font-weight: 600;'>{st.session_state.username}!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Theme switcher with custom styling
        st.markdown("<p style='color: #00d4ff;'>🎨 Theme</p>", unsafe_allow_html=True)
        theme = st.selectbox("", ["Dark", "Light"], label_visibility="collapsed")
        if theme == "Light":
            apply_custom_theme("light")
        
        st.markdown("---")
        
        # Navigation with custom styling
        st.markdown("<p style='color: #00d4ff;'>🧭 Navigation</p>", unsafe_allow_html=True)
        page = st.radio(
            "",
            ["📊 Dashboard", "🎓 Study Room (AI Mentor)", "🔥 Progress Heatmap", "👤 Profile"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick stats with custom styling
        st.markdown("<p style='color: #00d4ff;'>📊 Quick Stats</p>", unsafe_allow_html=True)
        progress = db.get_user_progress(st.session_state.user_id)
        if progress:
            topics_studied = len(progress)
            avg_mastery = sum(p[1] for p in progress) / topics_studied
            
            # Metric cards
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div style='background: #16213e; padding: 10px; border-radius: 10px; border: 1px solid #00d4ff; text-align: center;'>
                    <p style='color: #00d4ff; margin: 0; font-size: 12px;'>Topics</p>
                    <p style='color: #ffffff; margin: 0; font-size: 24px; font-weight: 600;'>{topics_studied}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background: #16213e; padding: 10px; border-radius: 10px; border: 1px solid #00d4ff; text-align: center;'>
                    <p style='color: #00d4ff; margin: 0; font-size: 12px;'>Mastery</p>
                    <p style='color: #ffffff; margin: 0; font-size: 24px; font-weight: 600;'>{avg_mastery:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Logout button with custom styling
        if st.button("🚪 Logout", use_container_width=True):
            for key in ['authenticated', 'user_id', 'username', 'mentor']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
        
        # Footer in sidebar
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center;'>
            <a href="#" style='color: #00d4ff; font-size: 24px; margin: 0 10px;'><i class="fab fa-linkedin"></i></a>
            <a href="#" style='color: #00d4ff; font-size: 24px; margin: 0 10px;'><i class="fab fa-instagram"></i></a>
            <a href="#" style='color: #00d4ff; font-size: 24px; margin: 0 10px;'><i class="fab fa-github"></i></a>
            <p style='color: #ffffff; margin-top: 10px;'>Made with ❤️ by Nishant</p>
        </div>
        """, unsafe_allow_html=True)
        
        return page.split(" ", 1)[1]  # Remove emoji and return page name
