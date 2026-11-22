import streamlit as st
st.set_page_config(page_title="Electrical Simulator", layout="wide")
st.title("⚡ Electrical Simulator PRO")
st.write("DOL • Star-Delta • Forward/Reverse • Timers • Motors")

mode = st.selectbox("Choose Circuit", ["DOL Starter", "Star-Delta", "Forward / Reverse", "Timer ON/OFF", "Single Phase", "2-Speed Motor", "Auto Transformer", "Soft Starter"])

col1, col2 = st.columns(2)
with col1:
    if st.button("▶ START", use_container_width=True):
        st.session_state.running = True
    if st.button("■ STOP", use_container_width=True):
        st.session_state.running = False
with col2:
    overload = st.slider("Overload Current (A)", 2, 30, 10)
    timer = st.slider("Timer Delay (s)", 1, 15, 5)
    load = st.slider("Motor Load %", 0, 100, 50)

running = st.session_state.get("running", False)

if running:
    st.success(f"✅ Motor RUNNING - {mode} - Load {load}% - Overload {overload}A")
    st.markdown("<h1 style='text-align:center'>⚙️ 🔄</h1>", unsafe_allow_html=True)
    st.write(f"Contactor: CLOSED | Timer: {timer}s")
    if st.button("⚠ TRIP OVERLOAD"):
        st.error("OVERLOAD TRIPPED! Motor stopped.")
        st.session_state.running = False
else:
    st.info("Motor Stopped - Press START")
    st.markdown("<h1 style='text-align:center'>⚙️</h1>", unsafe_allow_html=True)

st.markdown("---")
st.write("**Components:** Contactor K1/K2/K3 + 4-Contact, Overload Relay, 1-Phase Motor, 3-Phase Motor, 2-Speed Motor, Auxiliary, Buzzer, Lamps, Timer ON/OFF, 1/2/3 Pole MCB")
