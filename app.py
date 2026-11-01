import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bloxstrike Profit Calculator", page_icon="💰", layout="wide")

st.markdown("""
<style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1200px;}
    [data-testid="stMetric"] {background: rgba(128,128,128,.08); padding: 14px 16px; border-radius: 12px;}
    .small-note {opacity: .72; font-size: .88rem;}
</style>
""", unsafe_allow_html=True)

st.title("💰 Bloxstrike Profit Calculator")
st.caption("Calcola costi, ricavi, commissioni e profitti in USD. Tutti i valori sono modificabili.")

FEE_DEFAULT = 15.0

def money(value):
    return f"${value:,.4f}" if abs(value) < 1 else f"${value:,.2f}"

def profit_metrics(cost, revenue, fee_pct):
    fee = revenue * fee_pct / 100
    net_revenue = revenue - fee
    net_profit = net_revenue - cost
    margin = (net_profit / cost * 100) if cost else 0.0
    return fee, net_revenue, net_profit, margin

with st.sidebar:
    st.header("⚙️ Impostazioni")
    fee_pct = st.number_input("Commissione sulla vendita (%)", min_value=0.0, max_value=100.0,
                              value=FEE_DEFAULT, step=0.5)
    st.caption("La commissione viene calcolata sul prezzo totale di vendita.")
    st.divider()
    st.caption("Valuta: USD ($)")

tab_tokens, tab_cases, tab_guide = st.tabs(["🪙 Token", "📦 Casse Bloxstrike", "💡 Prezzi e guida"])

with tab_tokens:
    st.subheader("Calcolatore token")
    st.write("Inserisci quanto paghi per 1.000 token e il prezzo al quale rivendi ogni token.")
    c1, c2, c3 = st.columns(3)
    with c1:
        cost_1000 = st.number_input("Costo di acquisto per 1.000 token ($)", min_value=0.0,
                                    value=1.00, step=0.05, format="%.4f")
    with c2:
        sell_each = st.number_input("Prezzo di vendita per token ($)", min_value=0.0,
                                    value=0.0045, step=0.0001, format="%.4f")
    with c3:
        qty = st.selectbox("Quantità da calcolare", [500, 1000, 5000, 10000], index=0)

    cost = cost_1000 * qty / 1000
    revenue = sell_each * qty
    fee, net_revenue, net_profit, margin = profit_metrics(cost, revenue, fee_pct)

    st.markdown("#### Risultato")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Costo totale", money(cost))
    m2.metric("Ricavo lordo", money(revenue))
    m3.metric(f"Commissione ({fee_pct:g}%)", money(fee))
    m4.metric("Profitto netto", money(net_profit), delta=f"{margin:.2f}% sul costo")
    st.info(f"Dopo la commissione ti rimangono **{money(net_revenue)}**. Tolto il costo dei token, il profitto effettivo è **{money(net_profit)}**.")

    st.markdown("#### Confronto quantità")
    rows = []
    for q in [500, 1000, 5000, 10000]:
        c = cost_1000 * q / 1000
        r = sell_each * q
        f, nr, p, mar = profit_metrics(c, r, fee_pct)
        rows.append({"Token": q, "Costo": c, "Ricavo lordo": r, "Fee": f,
                     "Ricavo dopo fee": nr, "Profitto netto": p, "Margine sul costo": mar})
    df = pd.DataFrame(rows)
    st.dataframe(df.style.format({
        "Costo": "${:.4f}", "Ricavo lordo": "${:.4f}", "Fee": "${:.4f}",
        "Ricavo dopo fee": "${:.4f}", "Profitto netto": "${:.4f}",
        "Margine sul costo": "{:.2f}%"
    }), use_container_width=True, hide_index=True)

    st.markdown("#### Simulatore prezzi di vendita")
    st.caption("Confronta il risultato per token a diversi prezzi, mantenendo invariati costo e commissione.")
    price_options = [0.0035, 0.0040, 0.0045, 0.0050, 0.0055, 0.0060, 0.0070, 0.0080]
    price_rows = []
    for p_each in price_options:
        r = p_each * qty
        f, nr, p, mar = profit_metrics(cost, r, fee_pct)
        price_rows.append({"Prezzo/token": p_each, "Ricavo lordo": r, "Fee": f,
                           "Profitto netto": p, "Margine sul costo": mar})
    price_df = pd.DataFrame(price_rows)
    st.dataframe(price_df.style.format({
        "Prezzo/token": "${:.4f}", "Ricavo lordo": "${:.4f}", "Fee": "${:.4f}",
        "Profitto netto": "${:.4f}", "Margine sul costo": "{:.2f}%"
    }), use_container_width=True, hide_index=True)

    if cost > 0:
        break_even = cost / (qty * (1 - fee_pct / 100)) if fee_pct < 100 else 0
        st.success(f"Prezzo minimo per non andare in perdita: **${break_even:.6f} per token** (commissione inclusa).")
    else:
        st.warning("Inserisci un costo di acquisto maggiore di zero per calcolare il prezzo di pareggio.")

with tab_cases:
    st.subheader("Calcolatore casse Bloxstrike")
    st.write("Imposta il costo e il prezzo di vendita di una singola cassa. I calcoli si aggiornano per x1, x10, x50 e x100.")
    a, b = st.columns(2)
    with a:
        buy_case = st.number_input("Prezzo di acquisto per 1 cassa ($)", min_value=0.0,
                                   value=0.50, step=0.05, format="%.4f")
    with b:
        sell_case = st.number_input("Prezzo di vendita per 1 cassa ($)", min_value=0.0,
                                    value=0.75, step=0.05, format="%.4f")
    selected_qty = st.selectbox("Quantità casse", [1, 10, 50, 100], index=0, key="case_qty")
    total_cost = buy_case * selected_qty
    total_revenue = sell_case * selected_qty
    fee, net_revenue, net_profit, margin = profit_metrics(total_cost, total_revenue, fee_pct)

    x1, x2, x3, x4 = st.columns(4)
    x1.metric("Costo totale", money(total_cost))
    x2.metric("Ricavo lordo", money(total_revenue))
    x3.metric(f"Fee ({fee_pct:g}%)", money(fee))
    x4.metric("Profitto netto", money(net_profit), delta=f"{margin:.2f}% sul costo")

    st.markdown("#### Tabella quantità")
    case_rows = []
    for q in [1, 10, 50, 100]:
        c = buy_case * q
        r = sell_case * q
        f, nr, p, mar = profit_metrics(c, r, fee_pct)
        case_rows.append({"Quantità": f"x{q}", "Costo totale": c, "Ricavo lordo": r,
                          "Commissione": f, "Ricavo dopo fee": nr,
                          "Profitto netto": p, "Margine sul costo": mar})
    case_df = pd.DataFrame(case_rows)
    st.dataframe(case_df.style.format({
        "Costo totale": "${:.2f}", "Ricavo lordo": "${:.2f}", "Commissione": "${:.2f}",
        "Ricavo dopo fee": "${:.2f}", "Profitto netto": "${:.2f}",
        "Margine sul costo": "{:.2f}%"
    }), use_container_width=True, hide_index=True)

    if buy_case > 0:
        case_break_even = buy_case / (1 - fee_pct / 100) if fee_pct < 100 else 0
        st.success(f"Prezzo minimo di vendita per cassa per andare in pari: **{money(case_break_even)}**.")
    else:
        st.warning("Inserisci un costo di acquisto maggiore di zero per calcolare il prezzo di pareggio.")

with tab_guide:
    st.subheader("Come leggere i risultati")
    st.markdown("""
    - **Costo totale:** quanto spendi per acquistare token o casse.
    - **Ricavo lordo:** prezzo di vendita moltiplicato per la quantità.
    - **Commissione:** percentuale trattenuta dalla piattaforma sul ricavo lordo.
    - **Ricavo dopo fee:** denaro che ricevi dopo la commissione.
    - **Profitto netto:** ricavo dopo fee meno costo di acquisto.
    - **Margine sul costo:** profitto netto diviso costo di acquisto, espresso in percentuale.

    **Consiglio:** usa il prezzo minimo di pareggio come soglia, non come prezzo consigliato.
    Per scegliere il prezzo finale, confronta i profitti nella tabella e considera anche la velocità
    con cui riesci effettivamente a vendere. Un prezzo più alto non garantisce più vendite.
    """)

st.divider()
st.caption("Calcolatore indicativo: verifica sempre eventuali costi aggiuntivi, conversioni valutarie o regole della piattaforma.")
