import streamlit as st
from inference import inference

# Start execution
def main():
    # Render mardown text
    f = open("intro.md", 'r')
    readme_text = st.markdown(f.read())
    f.close()
    run_app()

# Main app
def run_app():
    # Input from user
    user_input = st.text_area("Type in your thoughts here")

    if user_input:
        # Display rediction as table
        if inference(user_input)[0] == 1:
          st.write("Your input indicates a sign of stress. If you think you're suffering from stress, anxiety, or any other medical health condition, please seek help from a mental health professional in order to receive a proper diagnosis and support.")
        else:
          st.write("Great! Your input doesn't show any signs of stress.")

if __name__ == "__main__":
    # execute only if run as a script
    main()
