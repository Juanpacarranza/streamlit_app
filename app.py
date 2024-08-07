import streamlit as st
from streamlit_option_menu import option_menu
import authentication

# Manejar redirección desde Azure AD
query_params = st.query_params
code = query_params["code"] if "code" in query_params else None
if "code" in query_params:
    authentication.handle_redirect()
else:
    st.error("")

if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.warning("You are not logged in")
    
    # Mostrar botón de inicio de sesión
    if "auth_uri" in st.session_state:
        st.markdown(f"[Log in with Microsoft]({st.session_state['auth_uri']})")
    else:
        authentication.authenticate_user()
    st.stop()
else:
    st.success(f"Welcome!")
    # Aquí se muestra contenido protegido o se redirige a la página principal

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
        """
    )
