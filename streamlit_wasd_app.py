import streamlit as st
import time
import threading
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(
    page_title="Auto WASD Program - Web Version",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS untuk styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    
    .status-running {
        color: #28a745;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .status-stopped {
        color: #dc3545;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    .current-key {
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        color: #007bff;
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #e9ecef;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
    }
    
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inisialisasi session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'current_key_index' not in st.session_state:
    st.session_state.current_key_index = 0
if 'keys' not in st.session_state:
    st.session_state.keys = ['W', 'A', 'S', 'D']
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'key_count' not in st.session_state:
    st.session_state.key_count = 0

# Judul utama
st.markdown('<h1 class="main-title">🎮 Auto WASD Program - Web Version</h1>', unsafe_allow_html=True)

# Warning box
st.markdown("""
<div class="warning-box">
    <strong>⚠️ Catatan Penting:</strong><br>
    Ini adalah versi web demo dari aplikasi Auto WASD. Fungsi penekanan tombol otomatis tidak dapat berjalan di lingkungan web browser karena keterbatasan keamanan. Aplikasi ini hanya menampilkan simulasi antarmuka untuk tujuan demonstrasi.
</div>
""", unsafe_allow_html=True)

# Kolom untuk layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Method selection
    st.subheader("🔧 Input Method")
    method = st.radio(
        "Pilih method input:",
        ["pynput (Recommended for games)", "pyautogui (Standard)"],
        index=0
    )
    
    st.markdown("---")
    
    # Status display
    st.subheader("📊 Status")
    if st.session_state.running:
        st.markdown('<p class="status-running">Status: Running (Web Demo)</p>', unsafe_allow_html=True)
        
        # Current key display
        current_key = st.session_state.keys[st.session_state.current_key_index]
        st.markdown(f'<div class="current-key">Current Key: {current_key}</div>', unsafe_allow_html=True)
        
        # Statistics
        if st.session_state.start_time:
            elapsed_time = time.time() - st.session_state.start_time
            st.metric("⏱️ Waktu Berjalan", f"{elapsed_time:.1f} detik")
            st.metric("🔢 Total Key Presses", st.session_state.key_count)
            
        # Next key info
        next_key_index = (st.session_state.current_key_index + 1) % len(st.session_state.keys)
        next_key = st.session_state.keys[next_key_index]
        st.info(f"Next Key: {next_key}")
        
    else:
        st.markdown('<p class="status-stopped">Status: Stopped</p>', unsafe_allow_html=True)
        st.markdown('<div class="current-key">Current Key: None</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Control buttons
    st.subheader("🎮 Controls")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("▶️ Play", disabled=st.session_state.running, use_container_width=True):
            st.session_state.running = True
            st.session_state.start_time = time.time()
            st.session_state.key_count = 0
            st.session_state.current_key_index = 0
            st.success("Program dimulai! (Demo mode)")
            st.rerun()
    
    with col_btn2:
        if st.button("⏹️ Stop", disabled=not st.session_state.running, use_container_width=True):
            st.session_state.running = False
            st.session_state.start_time = None
            st.warning("Program dihentikan!")
            st.rerun()

# Auto-refresh untuk simulasi
if st.session_state.running:
    # Simulasi pergantian key setiap 0.5 detik
    time.sleep(0.5)
    st.session_state.current_key_index = (st.session_state.current_key_index + 1) % len(st.session_state.keys)
    st.session_state.key_count += 1
    st.rerun()

# Informasi aplikasi
st.markdown("---")
st.markdown("""
<div class="info-box">
    <h4>📋 Informasi Aplikasi</h4>
    <ul>
        <li><strong>Interval:</strong> 0.5 detik per tombol</li>
        <li><strong>Urutan:</strong> W → A → S → D (repeat)</li>
        <li><strong>Platform:</strong> Web Demo (Streamlit)</li>
        <li><strong>Fungsi:</strong> Simulasi antarmuka saja</li>
    </ul>
    
    <h4>🚀 Untuk Aplikasi Desktop Asli:</h4>
    <ul>
        <li>Download file Python asli</li>
        <li>Install dependencies: <code>pip install pynput pyautogui tkinter</code></li>
        <li>Jalankan: <code>python WASD_Auto_Presser.py</code></li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c757d; font-size: 0.9rem;">
    <p>🎮 Auto WASD Program - Web Version | Made with Streamlit</p>
    <p>⚠️ Ini adalah demo web. Untuk fungsi penuh, gunakan aplikasi desktop.</p>
</div>
""", unsafe_allow_html=True)

