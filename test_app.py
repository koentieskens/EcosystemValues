import streamlit as st

class Test_App:

    def __init__(self):
        self.var1 = 0

    def run(self):
        st.title("Test App")
        st.write("This is a test app")

    def test_function(self):
        self.var1 += 1

    def write_var1(self):
        st.write(str(self.var1))




def main():
    try:
        st.set_page_config(
            page_title="Ecosystem Valuation Tool",
            page_icon="🌱",
            layout="wide"
        )
    except:
        pass  # Ignore if not supported in older Streamlit versions

    st.title("🌱 Ecosystem Valuation Tool")
    st.markdown("---")

    if 'instantiated' not in st.session_state:
        st.session_state.instantiated = False

    if not st.session_state.instantiated:
        st.session_state.test_app = Test_App()
        st.session_state.instantiated = True

    st.session_state.test_app.write_var1()

    if st.button("Add one"):
        st.session_state.test_app.test_function()
        st.rerun()


if __name__ == "__main__":
    main()