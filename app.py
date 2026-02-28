import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
import database as db
import auth
import ui_components as ui
from ai_engine import SocraticMentor, get_rubric_feedback
import utils

load_dotenv()

st.set_page_config(
    page_title="Saarthi AI - Thinking Coach",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


db.init_database()


utils.initialize_session_state()


ui.apply_custom_theme("dark")


def main():
   
    if not st.session_state.authenticated:
        # Show login/signup page
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <h1 style='text-align: center; color: #00d4ff; margin-bottom: 30px;'>
                🎓 Saarthi AI
            </h1>
            <p style='text-align: center; color: #ffffff; margin-bottom: 30px;'>
                Your Personal Thinking Coach
            </p>
            """, unsafe_allow_html=True)
        
        auth.login_signup_page()
        return
    
    # User is authenticated, show main app
    page = ui.render_sidebar()
    
    # Render selected page
    if "Dashboard" in page:
        render_dashboard()
    elif "Study Room" in page:
        render_study_room()
    elif "Progress Heatmap" in page:
        render_progress()
    elif "Profile" in page:
        render_profile()

def render_dashboard():
    """Render the dashboard page"""
    
    st.markdown(f"## 📊 Welcome back, {st.session_state.username}!")
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        progress = db.get_user_progress(st.session_state.user_id)
        topics_count = len(progress) if progress else 0
        st.metric("Topics Studied", topics_count, delta=None)
    
    with col2:
        chat_history = db.get_chat_history(st.session_state.user_id, limit=1000)
        total_interactions = len(chat_history) if chat_history else 0
        st.metric("Total Interactions", total_interactions, delta=None)
    
    with col3:
        if progress:
            avg_mastery = sum(p[1] for p in progress) / len(progress)
            st.metric("Average Mastery", f"{avg_mastery:.1f}%")
        else:
            st.metric("Average Mastery", "0%")
    
    with col4:
        st.metric("Current Doubt Score", f"{st.session_state.doubt_score}%")
    
    st.markdown("---")
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🕒 Recent Activity")
        if chat_history:
            for role, msg, topic, timestamp in chat_history[:5]:
                if role == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <small>{utils.format_timestamp(timestamp)}</small><br>
                        <b>You asked about {topic}:</b> {utils.truncate_text(msg)}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No recent activity. Start learning in the Study Room!")
    
    with col2:
        st.markdown("### 🎯 Current Focus")
        if progress:
            # Show topics needing attention
            low_mastery = [p for p in progress if p[1] < 50]
            if low_mastery:
                st.markdown("**Topics needing practice:**")
                for topic, mastery, _, _ in low_mastery[:3]:
                    st.progress(mastery/100, text=f"{topic}: {mastery}%")
            else:
                st.success("Great job! All topics are above 50% mastery!")
        else:
            st.info("Start learning to track your progress!")

def render_study_room():
    """Render the AI mentor study room"""
    
    st.markdown("## 🎓 Study Room - AI Mentor")
    
    # Initialize mentor if not exists
    if st.session_state.mentor is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            st.error("Please set your GEMINI_API_KEY in .env file")
            return
        st.session_state.mentor = SocraticMentor(api_key)
    
    # Mode selection
    mode = st.radio(
        "Select Mode",
        ["💭 Socratic Mentor", "📝 Rubric Feedback"],
        horizontal=True,
        key="study_mode"
    )
    
    if mode == "💭 Socratic Mentor":
        render_socratic_mode()
    else:
        render_rubric_mode()

def render_socratic_mode():
    """Render the Socratic mentoring mode"""
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        # Doubt score gauge
        st.markdown('<div class="gauge-container">', unsafe_allow_html=True)
        gauge = ui.create_doubt_gauge(st.session_state.doubt_score)
        st.plotly_chart(gauge, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tips
        st.markdown("### 💡 Tips")
        st.info(
            """
            • Ask questions in Hindi/English
            • The mentor will guide you step by step
            • After 3-4 exchanges, you'll get the answer
            • Ask for hints if you're stuck
            """
        )
    
    with col1:
        # Chat interface
        st.markdown("### 💬 Chat with your Mentor")
        
        # Display chat history
        chat_history = db.get_chat_history(st.session_state.user_id, limit=20)
        if chat_history:
            for role, msg, topic, timestamp in reversed(chat_history):
                if role == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <b>You:</b> {msg}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="assistant-message">
                        <b>Mentor:</b> {msg}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        user_input = st.chat_input("Ask your question...")
        
        if user_input:
            # Display user message
            st.markdown(f"""
            <div class="user-message">
                <b>You:</b> {user_input}
            </div>
            """, unsafe_allow_html=True)
            
            # Get AI response
            with st.spinner("Thinking..."):
                response, doubt_score, topic = st.session_state.mentor.get_response(
                    user_input, 
                    st.session_state.user_id
                )
                st.session_state.doubt_score = doubt_score
            
            # Display response
            st.markdown(f"""
            <div class="assistant-message">
                <b>Mentor:</b> {response}
            </div>
            """, unsafe_allow_html=True)
            
            # refresh
            st.rerun()

def render_rubric_mode():
    """Render the rubric feedback mode"""
    
    st.markdown("### 📝 Get Structured Feedback")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        text_type = st.selectbox(
            "Select content type",
            ["essay", "code"]
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Get Feedback", type="primary", use_container_width=True):
            st.session_state.rubric_mode = True
    
    # Input as Text
    text_input = st.text_area(
        "Paste your essay or code here:",
        height=300,
        key="rubric_text_input"
    )
    
    if st.session_state.rubric_mode and text_input:
        st.markdown("---")
        st.markdown("### 📊 Feedback Analysis")
        
        with st.spinner("Analyzing..."):
            # Get feedback prompt
            prompt = get_rubric_feedback(text_input, text_type)
            
            # Get response
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                
                # Display feedback
                st.markdown(response.text)
                
                # Save to chat history
                db.save_chat_message(
                    st.session_state.user_id,
                    "user",
                    f"[Rubric Feedback Request] {text_type}",
                    "feedback"
                )
                db.save_chat_message(
                    st.session_state.user_id,
                    "assistant",
                    response.text,
                    "feedback"
                )
        
        st.session_state.rubric_mode = False

def render_progress():
    """Render the progress heatmap page"""
    
    st.markdown("## 🔥 Progress Heatmap")
    
    # Get user progress
    progress = db.get_user_progress(st.session_state.user_id)
    
    if not progress:
        st.info("No progress data yet. Start learning in the Study Room!")
        return
    
    # Mastery heatmap
    st.markdown('<p class="heatmap-title">Topic Mastery Overview</p>', 
                unsafe_allow_html=True)
    
    heatmap = ui.create_mastery_heatmap(st.session_state.user_id)
    if heatmap:
        st.plotly_chart(heatmap, use_container_width=True)
    
    # Detailed progress table
    st.markdown("### 📊 Detailed Progress")
    
    # Create DataFrame for display
    import pandas as pd
    df = pd.DataFrame(progress, columns=['Topic', 'Mastery', 'Interactions', 'Last Studied'])
    df['Mastery'] = df['Mastery'].apply(lambda x: f"{x}%")
    df['Last Studied'] = pd.to_datetime(df['Last Studied']).dt.strftime('%Y-%m-%d %H:%M')
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Topic": "Topic",
            "Mastery": "Mastery Level",
            "Interactions": "Interactions",
            "Last Studied": "Last Studied"
        }
    )
    
    # Study streak
    st.markdown("###  Study Streak")
    
    # Get chat history for streak calculation
    chat_history = db.get_chat_history(st.session_state.user_id)
    if chat_history:
        # Extract dates
        dates = [entry[3] for entry in chat_history]  # timestamp is at index 3
        dates = [pd.to_datetime(d).date() for d in dates]
        
        # Calculate streak
        unique_dates = sorted(set(dates), reverse=True)
        streak = 0
        current_date = pd.Timestamp.now().date()
        
        for date in unique_dates:
            if date == current_date:
                streak += 1
                current_date -= pd.Timedelta(days=1)
            else:
                break
        
        col1, col2, col3 = st.columns(3)
        with col2:
            st.metric("Current Streak", f"{streak} days")
    else:
        st.info("Start learning to build your streak!")

def render_profile():
    """Render the user profile page"""
    
    st.markdown("## 👤 Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        <div style='text-align: center;'>
            <div style='font-size: 100px;'>🎓</div>
            <h3>{}</h3>
        </div>
        """.format(st.session_state.username), unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Account Information")
        
        # Get user stats
        chat_history = db.get_chat_history(st.session_state.user_id, limit=1000)
        total_chats = len(chat_history) if chat_history else 0
        
        progress = db.get_user_progress(st.session_state.user_id)
        topics = len(progress) if progress else 0
        
        # Display stats
        stats_df = pd.DataFrame({
            "Metric": ["Username", "Total Chats", "Topics Studied", "Member Since"],
            "Value": [
                st.session_state.username,
                total_chats,
                topics,
                "Recent"  # Could fetch from database
            ]
        })
        st.dataframe(stats_df, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    # Theme preference (already in sidebar)
    st.info("Theme preference can be changed in the sidebar.")
    
    # Delete account option
    with st.expander("⚠️ Danger Zone"):
        st.warning("This action cannot be undone!")
        if st.button("Delete Account", type="primary", use_container_width=True):
            # Add account deletion logic here
            st.error("Account deletion is not implemented in this demo.")

if __name__ == "__main__":
    main()
