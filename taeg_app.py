
import streamlit as st
from scipy.optimize import newton

# Funzione per l'equazione del TAEG
def taeg_equation(taeg, rata, num_rate, freq_rate, importo_prestito, spese):
    total = 0
    for i in range(1, num_rate + 1):
        t = i / freq_rate  # tempo in anni
        total += rata / ((1 + taeg) ** t)
    return total - (importo_prestito - spese)

# Funzione per calcolare il TAEG
def calcola_taeg(importo_prestito, rata, num_rate, freq_rate=12, spese=0.0):
    try:
        taeg = newton(
            taeg_equation,
            0.05,
            args=(rata, num_rate, freq_rate, importo_prestito, spese)
        )
        return taeg
    except RuntimeError:
        return None

# Streamlit UI
st.set_page_config(page_title="Calcolatore TAEG", layout="centered")
st.title("Calcolatore TAEG")
st.markdown("Calcola il TAEG di un prestito a partire da importo, rata, durata e spese iniziali.")

with st.form("taeg_form"):
    importo = st.number_input("Importo del prestito (€)", min_value=0.0, value=10000.0, step=100.0)
    rata = st.number_input("Importo rata mensile (€)", min_value=0.0, value=200.0, step=10.0)
    durata_mesi = st.number_input("Durata (mesi)", min_value=1, value=60, step=1)
    spese = st.number_input("Spese accessorie iniziali (€)", min_value=0.0, value=300.0, step=10.0)
    submitted = st.form_submit_button("Calcola TAEG")

if submitted:
    taeg = calcola_taeg(importo, rata, durata_mesi, 12, spese)
    if taeg is not None:
        st.success(f"TAEG calcolato: {taeg * 100:.2f}%")
        st.markdown(f"**Dati inseriti:**\n- Importo prestito: €{importo:,.2f}\n- Rata mensile: €{rata:,.2f}\n- Durata: {durata_mesi} mesi\n- Spese: €{spese:,.2f}")
    else:
        st.error("Errore nel calcolo del TAEG. Riprova con altri valori.")
