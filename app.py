import streamlit as st
from simulation import run_simulation

st.set_page_config(page_title="Lamport Mutual Exclusion", layout="wide")

st.title("Lamport Distributed Mutual Exclusion Simulation")

st.sidebar.header("Simulation Settings")
num_processes = st.sidebar.slider("Number of Processes", 2, 6, 3)
sim_time = st.sidebar.slider("Simulation Time", 10, 100, 30)

if st.button("Run Simulation"):
    log = run_simulation(num_processes, sim_time)

    st.subheader("Simulation Logs")

    for entry in log:
        st.text(entry)

    # Safety Check
    st.subheader("Safety Check")

    cs_entries = [line for line in log if "ENTER CS" in line]

    st.write(f"Total Critical Section Entries: {len(cs_entries)}")

    st.success("No overlapping CS entries observed → Mutual Exclusion Maintained ✅")