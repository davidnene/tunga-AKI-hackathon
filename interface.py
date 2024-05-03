import streamlit as st
import pandas as pd
import json

from agent import query_agent, create_agent

def decode_response(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    return json.loads(response)


def write_response(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)

def handle_history():
    if st.session_state.chat_history:
        for i,message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write( message)
            else:
                st.write(message)

def main():

    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "data" not in st.session_state:
        st.session_state.data = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    
    st.title("👨‍💻 Insurance Data Chatbot")
    with st.sidebar:
        st.session_state.data = st.file_uploader("Upload your Insurance CSV")
        if st.button("Initiate agent"):
            with st.spinner("Initiating.."):
                st.session_state.agent = create_agent(st.session_state.data)
                st.success('Agent successfully initiated!', icon="✅")

    query = st.text_input("What would you like to ask?")
    
    # # Create an agent from the CSV file.
    # if not query and not st.session_state.data:
    #     st.warning("Please upload csv and initiate agent", icon='⚠️')
    # elif not query and st.session_state.data !=None:
    #     st.warning("Please ask a question", icon='⚠️')
    # else:
    #     # Query the agent.
    if st.button("query"):
        try:
            if not query and not st.session_state.data:
                st.warning("Please upload csv and initiate agent", icon='⚠️')
            elif not query and st.session_state.data !=None:
                st.warning("Please ask a question", icon='⚠️')
            else:
                st.session_state.chat_history.append(query)
                response = query_agent(agent=st.session_state.agent, query=query)
                # Decode the response.
                decoded_response = decode_response(response)
                # Write the response to the Streamlit app.
                st.session_state.chat_history.append(response)
                write_response(decoded_response)
        except:
            # st.write(e)
            st.warning("Please upload csv and initiate agent", icon='⚠️')
        
    if st.checkbox("show history"):
        handle_history()
        if st.button("clear history"):
            st.session_state.chat_history = []


if __name__ == '__main__':
    main()
