import streamlit as st
import database as db
import time

def login_signup_page():
    """Render the login/signup page with custom styling"""
    
    # Custom CSS for the login page
    st.markdown("""
    <style>
        /* Main container */
        .main {
            background-color: #1a1a2e;
        }
        
        /* Login container */
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 40px 30px;
            background: #16213e;
            border-radius: 15px;
            border: 2px solid #00d4ff;
            box-shadow: 0 0 30px #00d4ff;
            position: relative;
            overflow: hidden;
        }
        
        /* Title */
        .login-title {
            text-align: center;
            color: #00d4ff;
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        /* Subtitle */
        .login-subtitle {
            text-align: center;
            color: #ffffff;
            font-size: 16px;
            margin-bottom: 40px;
            opacity: 0.8;
        }
        
        /* Form fields */
        .stTextInput > div > div > input {
            background: transparent !important;
            border: none !important;
            border-bottom: 2px solid #ffffff !important;
            border-radius: 0 !important;
            color: #ffffff !important;
            font-size: 16px !important;
            padding: 10px 0 !important;
            margin: 10px 0 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-bottom: 2px solid #00d4ff !important;
            box-shadow: none !important;
        }
        
        .stTextInput > div > div > label {
            color: #ffffff !important;
            font-size: 14px !important;
            transform: translateY(0) !important;
        }
        
        /* Icons for input fields */
        .input-icon {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: #00d4ff;
        }
        
        /* Button styling */
        .stButton > button {
            background: transparent !important;
            border: 2px solid #00d4ff !important;
            color: #ffffff !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            padding: 12px !important;
            border-radius: 40px !important;
            width: 100%;
            margin-top: 20px !important;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background: #00d4ff !important;
            color: #1a1a2e !important;
            transform: scale(1.02);
            box-shadow: 0 0 20px #00d4ff;
        }
        
        /* Toggle link */
        .toggle-link {
            text-align: center;
            margin-top: 20px;
            color: #ffffff;
        }
        
        .toggle-link a {
            color: #00d4ff;
            text-decoration: none;
            font-weight: 600;
            cursor: pointer;
        }
        
        .toggle-link a:hover {
            text-decoration: underline;
        }
        
        /* Welcome text */
        .welcome-text {
            text-align: center;
            color: #00d4ff;
            font-size: 24px;
            font-weight: 600;
            margin: 20px 0;
            text-transform: uppercase;
        }
        
        /* Error message */
        .stAlert {
            background: rgba(255, 0, 0, 0.1) !important;
            border: 1px solid #ff0000 !important;
            color: #ffffff !important;
        }
        
        /* Success message */
        .stSuccess {
            background: rgba(0, 255, 0, 0.1) !important;
            border: 1px solid #00ff00 !important;
            color: #ffffff !important;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #ffffff;
            font-size: 14px;
        }
        
        .footer a {
            color: #00d4ff;
            text-decoration: none;
            font-weight: 600;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        /* Shape decorations */
        .shape {
            position: absolute;
            width: 300px;
            height: 300px;
            background: linear-gradient(45deg, #1a1a2e, #00d4ff);
            border-radius: 50%;
            filter: blur(50px);
            opacity: 0.3;
            z-index: -1;
        }
        
        .shape-1 {
            top: -100px;
            right: -100px;
        }
        
        .shape-2 {
            bottom: -100px;
            left: -100px;
        }
    </style>
    
    <!-- Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    """, unsafe_allow_html=True)
    
    # Initialize session state for toggling
    if 'auth_toggled' not in st.session_state:
        st.session_state.auth_toggled = False
    
    # Shapes for background
    st.markdown("""
    <div class="shape shape-1"></div>
    <div class="shape shape-2"></div>
    """, unsafe_allow_html=True)
    
    # Main container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="login-title">Saarthi AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-subtitle">Your Personal Thinking Coach</p>', unsafe_allow_html=True)
    
    # Toggle between Login and Register
    if not st.session_state.auth_toggled:
        # LOGIN FORM
        st.markdown('<h2 style="color: #00d4ff; text-align: center;">Login</h2>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            # Username with icon
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                username = st.text_input("Username", key="login_user", label_visibility="visible")
            with col2:
                st.markdown('<i class="fas fa-user" style="color: #00d4ff; font-size: 20px; margin-top: 15px;"></i>', unsafe_allow_html=True)
            
            # Password with icon
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                password = st.text_input("Password", type="password", key="login_pass", label_visibility="visible")
            with col2:
                st.markdown('<i class="fas fa-lock" style="color: #00d4ff; font-size: 20px; margin-top: 15px;"></i>', unsafe_allow_html=True)
            
            # Login button
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                user = db.login_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user[0]
                    st.session_state.username = user[1]
                    st.rerun()
                else:
                    st.error("Invalid username or password!")
        
        # Toggle to Register
        st.markdown("""
        <div class="toggle-link">
            Don't have an account? <br>
            <a href="#" onclick="toggleAuth()">Sign Up</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Welcome message
        st.markdown('<div class="welcome-text">WELCOME BACK!</div>', unsafe_allow_html=True)
        
    else:
        # REGISTER FORM
        st.markdown('<h2 style="color: #00d4ff; text-align: center;">Register</h2>', unsafe_allow_html=True)
        
        with st.form("register_form"):
            # Username with icon
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                username = st.text_input("Username", key="reg_user", label_visibility="visible")
            with col2:
                st.markdown('<i class="fas fa-user" style="color: #00d4ff; font-size: 20px; margin-top: 15px;"></i>', unsafe_allow_html=True)
            
            # Email with icon
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                email = st.text_input("Email", key="reg_email", label_visibility="visible")
            with col2:
                st.markdown('<i class="fas fa-envelope" style="color: #00d4ff; font-size: 20px; margin-top: 15px;"></i>', unsafe_allow_html=True)
            
            # Password with icon
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                password = st.text_input("Password", type="password", key="reg_pass", label_visibility="visible")
            with col2:
                st.markdown('<i class="fas fa-lock" style="color: #00d4ff; font-size: 20px; margin-top: 15px;"></i>', unsafe_allow_html=True)
            
            # Confirm Password with icon
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm", label_visibility="visible")
            with col2:
                st.markdown('<i class="fas fa-lock" style="color: #00d4ff; font-size: 20px; margin-top: 15px;"></i>', unsafe_allow_html=True)
            
            # Register button
            submitted = st.form_submit_button("Register", use_container_width=True)
            
            if submitted:
                if password != confirm_password:
                    st.error("Passwords don't match!")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters!")
                else:
                    success, message = db.register_user(username, email, password)
                    if success:
                        st.success(message)
                        st.session_state.auth_toggled = False
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)
        
        # Toggle to Login
        st.markdown("""
        <div class="toggle-link">
            Already have an account? <br>
            <a href="#" onclick="toggleAuth()">Sign In</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Welcome message
        st.markdown('<div class="welcome-text">WELCOME!</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # JavaScript for toggle functionality
    st.markdown("""
    <script>
    function toggleAuth() {
        const authToggled = window.parent.document.querySelector('[data-testid="stSessionState"]');
        if (authToggled) {
            const event = new Event('input', { bubbles: true });
            authToggled.value = !authToggled.value;
            authToggled.dispatchEvent(event);
        }
    }
    </script>
    
    <!-- Footer -->
    <div class="footer">
        <p>Made with ❤️ by <a href="#" target="_blank">Nishant</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Handle toggle via session state (since JavaScript won't work directly)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Switch to " + ("Login" if st.session_state.auth_toggled else "Register"), use_container_width=True):
            st.session_state.auth_toggled = not st.session_state.auth_toggled
            st.rerun()
