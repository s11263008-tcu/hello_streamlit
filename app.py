import streamlit as st

st.title("Hello, Streamlit!")

text = st.text_input("Enter whatever you want", key="name")

if st.button("Save to input.txt"):
    with open("input.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")
    st.success("Saved!")
    st.write(f"You entered: {text}")