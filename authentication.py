import streamlit as st
from msal import ConfidentialClientApplication
import settings

#--- // ---#
# Crear un cliente de autenticación utilizando MSAL (Microsoft Authentication Library)
# con la configuración proporcionada (ID de cliente, autoridad, secreto de cliente)
# Esto es esencial para interactuar con Azure AD y gestionar los tokens de acceso.

app = ConfidentialClientApplication(
    settings.CLIENT_ID,
    authority=settings.AUTHORITY,
    client_credential=settings.CLIENT_SECRET,
)

#--- // ---#
#  Iniciar el proceso de autenticación del usuario.

def authenticate_user():
    #  Define la URI de redirección a la que Azure AD enviará al usuario después de la autenticación.
    base_url = "http://localhost:8501" if settings.environment == 'dev' else "https://cost-simulation-app-vthhaczahnv7bajvcnwnmj.streamlit.app"
    redirect_uri = base_url  

    result = None # almacenara el token de acceso

    # Verifica si hay cuentas almacenadas y trata de adquirir un token en silencio 
    # (sin intervención del usuario) si ya hay una sesión activa

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(settings.SCOPES, account=accounts[0]) 
    # Si no hay token en la session se inicia el flujo de autenticacion
    # flow: Contiene información necesaria para completar el flujo de autenticación (state, redirect_uri, scope, auth_uri, code_verifier, nonce, claims_challenge)
    # Inicializar las claves necesarias en session_state
    if not result:
        flow = app.initiate_auth_code_flow(settings.SCOPES, redirect_uri=redirect_uri)
        st.session_state["flow"] = flow
        st.session_state["auth_uri"] = flow["auth_uri"]
        st.session_state["state"] = flow["state"]
        st.write("session state", st.session_state)
    
    return st.session_state
        
#--- // ---#

def handle_redirect():
    query_params = st.query_params
    code = query_params["code"] if "code" in query_params else None
    state = query_params["state"] if "state" in query_params else None
    st.write("session state 2", st.session_state) #Desde aca ya no se ve nada
    flow = st.session_state.get("flow", None)

    if not code or not state:
        st.error("Authorization code or state is missing.")
        return
    
    if not flow:
        st.error("flow is missing.")
        return


    try:
        result = app.acquire_token_by_authorization_code(
            code,  # El código de autorización obtenido
            scopes=settings.SCOPES,  # Los alcances que solicitaste
            redirect_uri=redirect_uri  # La misma URI de redirección utilizada en el flujo de solicitud inicial
        )
        if "access_token" in result:
            st.session_state["authenticated"] = True
            st.session_state["token"] = result
            st.success("Authentication successful!")
            return
        else:
            st.error(f"Failed to acquire tokens: {result.get('error_description')}")
            return
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    # HASTA AQUI YA HEMOS LOGRADO QUE SE EXTRAIGA EL CODE Y STATE DE LA REDIRECT_URI Y QUE 
    # AUTHENTICATE_USER DEVUELVA EVERYTHING LO QUE GUARDEMOS EN ST.SESSION_STATE. AHORA DEBEMOS
    # CAMBIAR EL CODIGO POR EL TOKEN - SEGURAMENTE TENDREMOS QUE GUARDAR EL FLOW COMPLETO EN ST.SESSION_STATE
    # Y RECUPERARLO EN HANDLE REDIRECT. 
    #st.write("Session state 2", st.session_state)

    #st.write("Query Params:", query_params)
    #st.write("Authorization Code:", code)
    #st.write("State:", state)

        # Intercambiar el código por un token de acceso