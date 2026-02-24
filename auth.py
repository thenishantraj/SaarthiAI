import streamlit as st
import database as db
import time

def login_signup_page():
    """Render the login/signup page with custom styling"""
    
    # Initialize session state for toggling between login and signup
    if 'auth_toggled' not in st.session_state:
        st.session_state.auth_toggled = False
    
    # Custom HTML/CSS for the authentication form
    auth_html = f"""
    <div class="auth-wrapper {'toggled' if st.session_state.auth_toggled else ''}">
        <div class="background-shape"></div>
        <div class="secondary-shape"></div>
        
        <!-- Login Panel -->
        <div class="credentials-panel signin">
            <h2 class="slide-element">Login</h2>
            <form id="loginForm" onsubmit="handleLogin(event)">
                <div class="field-wrapper slide-element">
                    <input type="text" id="login_username" required>
                    <label for="">Username</label>
                    <i class="fa-solid fa-user"></i>
                </div>

                <div class="field-wrapper slide-element">
                    <input type="password" id="login_password" required>
                    <label for="">Password</label>
                    <i class="fa-solid fa-lock"></i>
                </div>

                <div class="field-wrapper slide-element">
                    <button class="submit-button" type="submit">Login</button>
                </div>

                <div class="switch-link slide-element">
                    <p>Don't have an account? <br> <a href="#" onclick="toggleAuth(event)">Sign Up</a></p>
                </div>
            </form>
        </div>

        <div class="welcome-section signin">
            <h2 class="slide-element">WELCOME BACK!</h2>
        </div>

        <!-- Signup Panel -->
        <div class="credentials-panel signup">
            <h2 class="slide-element">Register</h2>
            <form id="signupForm" onsubmit="handleSignup(event)">
                <div class="field-wrapper slide-element">
                    <input type="text" id="signup_username" required>
                    <label for="">Username</label>
                    <i class="fa-solid fa-user"></i>
                </div>

                <div class="field-wrapper slide-element">
                    <input type="email" id="signup_email" required>
                    <label for="">Email</label>
                    <i class="fa-solid fa-envelope"></i>
                </div>

                <div class="field-wrapper slide-element">
                    <input type="password" id="signup_password" required>
                    <label for="">Password</label>
                    <i class="fa-solid fa-lock"></i>
                </div>

                <div class="field-wrapper slide-element">
                    <button class="submit-button" type="submit">Register</button>
                </div>

                <div class="switch-link slide-element">
                    <p>Already have an account? <br> <a href="#" onclick="toggleAuth(event)">Sign In</a></p>
                </div>
            </form>
        </div>

        <div class="welcome-section signup">
            <h2 class="slide-element">WELCOME!</h2>
        </div>
    </div>
    
    <div class="footer">
        <p>Made with ❤️ by <a href="#" target="_blank">Nishant</a></p>
    </div>
    
    <script>
        function toggleAuth(e) {{
            e.preventDefault();
            const wrapper = document.querySelector('.auth-wrapper');
            wrapper.classList.toggle('toggled');
            // Update Streamlit session state
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: wrapper.classList.contains('toggled')
            }}, '*');
        }}
        
        function handleLogin(e) {{
            e.preventDefault();
            const username = document.getElementById('login_username').value;
            const password = document.getElementById('login_password').value;
            
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                loginData: {{username: username, password: password}}
            }}, '*');
        }}
        
        function handleSignup(e) {{
            e.preventDefault();
            const username = document.getElementById('signup_username').value;
            const email = document.getElementById('signup_email').value;
            const password = document.getElementById('signup_password').value;
            
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                signupData: {{username: username, email: email, password: password}}
            }}, '*');
        }}
    </script>
    """
    
    # Display the auth form
    components = st.components.v1
    components.html(auth_html, height=600)
    
    # Handle form submissions
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("auth_form"):
            auth_mode = "signup" if st.session_state.auth_toggled else "login"
            
            if auth_mode == "login":
                username = st.text_input("Username", key="login_user")
                password = st.text_input("Password", type="password", key="login_pass")
                
                if st.form_submit_button("Login", use_container_width=True):
                    user = db.login_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user[0]
                        st.session_state.username = user[1]
                        st.rerun()
                    else:
                        st.error("Invalid username or password!")
            
            else:
                username = st.text_input("Username", key="signup_user")
                email = st.text_input("Email", key="signup_email")
                password = st.text_input("Password", type="password", key="signup_pass")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
                
                if st.form_submit_button("Register", use_container_width=True):
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
