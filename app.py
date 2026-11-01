
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Bloxstrike Profit Calculator",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}
[data-testid="stMetric"] {
    background: rgba(128,128,128,.08);
    padding: 14px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Bloxstrike Profit Calculator")
st.caption("Calcolo costi token, casse, commissioni e profitti netti.")


# ==========================================
# FUNZIONI
# ==========================================

def money(value):
    return f"${value:,.4f}" if abs(value) < 1 else f"${value:,.2f}"


def calculate(cost, revenue, fee_pct):
    fee = revenue * fee_pct / 100
    net_revenue = revenue - fee
    profit = net_revenue - cost
    margin = profit / cost * 100 if cost > 0 else 0

    return fee, net_revenue, profit, margin


# ==========================================
# SIDEBAR - PORTAFOGLIO
# ==========================================

with st.sidebar:

    st.header("🎒 Portafoglio token")

    owned_tokens = st.number_input(
        "Token attualmente posseduti",
        min_value=0,
        value=1000,
        step=100
    )

    total_spent = st.number_input(
        "Totale speso per questi token ($)",
        min_value=0.0,
        value=1.00,
        step=0.05,
        format="%.4f"
    )

    st.divider()

    st.header("⚙️ Commissioni")

    fee_pct = st.number_input(
        "Commissione sulle vendite (%)",
        min_value=0.0,
        max_value=100.0,
        value=15.0,
        step=0.5
    )


# ==========================================
# COSTO MEDIO PORTAFOGLIO
# ==========================================

average_token_cost = (
    total_spent / owned_tokens
    if owned_tokens > 0 else 0
)

st.subheader("📊 Riepilogo portafoglio")

c1, c2, c3 = st.columns(3)

c1.metric("Token posseduti", f"{owned_tokens:,.0f}")
c2.metric("Spesa totale", money(total_spent))
c3.metric(
    "Costo medio per 1.000 token",
    money(average_token_cost * 1000)
)


# ==========================================
# NAVIGAZIONE
# ==========================================

tab1, tab2, tab3 = st.tabs([
    "🪙 Acquisto e vendita token",
    "📦 Casse Bloxstrike",
    "💡 Guida"
])


# ==========================================
# TAB 1 - TOKEN
# ==========================================

with tab1:

    st.header("🪙 Calcolatore token")

    st.write(
        "Inserisci quanto paghi per acquistare i token "
        "e calcola il profitto ottenuto dalla rivendita."
    )

    col1, col2 = st.columns(2)

    with col1:

        buy_1000 = st.number_input(
            "Costo di acquisto per 1.000 token ($)",
            min_value=0.0,
            value=1.00,
            step=0.05,
            format="%.4f"
        )

    with col2:

        sell_price = st.number_input(
            "Prezzo di vendita per token ($)",
            min_value=0.0,
            value=0.0045,
            step=0.0001,
            format="%.4f"
        )

    quantity = st.selectbox(
        "Quantità token da calcolare",
        [500, 1000, 5000, 10000]
    )

    # COSTI E RICAVI

    token_cost = buy_1000 * quantity / 1000

    revenue = sell_price * quantity

    fee, net_revenue, profit, margin = calculate(
        token_cost,
        revenue,
        fee_pct
    )

    st.markdown("### Risultato")

    a, b, c, d = st.columns(4)

    a.metric("Costo acquisto", money(token_cost))
    b.metric("Ricavo lordo", money(revenue))
    c.metric("Commissione", money(fee))
    d.metric(
        "Profitto netto",
        money(profit),
        delta=f"{margin:.2f}% sul costo"
    )

    st.info(
        f"Dopo la commissione ricevi {money(net_revenue)}. "
        f"Il profitto effettivo è {money(profit)}."
    )

    # CONFRONTO 500 E 1000

    st.markdown("### Confronto quantità")

    rows = []

    for q in [500, 1000, 5000, 10000]:

        cost = buy_1000 * q / 1000
        rev = sell_price * q

        f, net, p, m = calculate(cost, rev, fee_pct)

        rows.append({
            "Token": q,
            "Costo acquisto": cost,
            "Ricavo lordo": rev,
            "Commissione": f,
            "Ricavo dopo fee": net,
            "Profitto netto": p,
            "Margine": m
        })

    st.dataframe(
        pd.DataFrame(rows).style.format({
            "Costo acquisto": "${:.4f}",
            "Ricavo lordo": "${:.4f}",
            "Commissione": "${:.4f}",
            "Ricavo dopo fee": "${:.4f}",
            "Profitto netto": "${:.4f}",
            "Margine": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # CONFRONTO PREZZI

    st.markdown("### Quale prezzo di vendita conviene?")

    prices = [
        0.0035,
        0.0040,
        0.0045,
        0.0050,
        0.0055,
        0.0060,
        0.0070,
        0.0080
    ]

    price_rows = []

    for price in prices:

        rev = price * quantity

        f, net, p, m = calculate(
            token_cost,
            rev,
            fee_pct
        )

        price_rows.append({
            "Prezzo per token": price,
            "Ricavo lordo": rev,
            "Commissione": f,
            "Profitto netto": p,
            "Margine": m
        })

    st.dataframe(
        pd.DataFrame(price_rows).style.format({
            "Prezzo per token": "${:.4f}",
            "Ricavo lordo": "${:.4f}",
            "Commissione": "${:.4f}",
            "Profitto netto": "${:.4f}",
            "Margine": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # PAREGGIO

    if fee_pct < 100:

        break_even = (
            (buy_1000 / 1000) /
            (1 - fee_pct / 100)
        )

        st.success(
            f"Prezzo minimo per non andare in perdita: "
            f"**${break_even:.6f} per token**."
        )


# ==========================================
# TAB 2 - CASSE BLOXSTRIKE
# ==========================================

with tab2:

    st.header("📦 Calcolatore casse Bloxstrike")

    st.write(
        "Il prezzo di acquisto delle casse è espresso in token. "
        "Il sistema converte automaticamente il costo in dollari "
        "utilizzando il costo medio del tuo portafoglio."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        case_token_cost = st.number_input(
            "Costo di acquisto di 1 cassa (token)",
            min_value=0.0,
            value=100.0,
            step=10.0
        )

    with col2:

        case_sell_price = st.number_input(
            "Prezzo di vendita di 1 cassa ($)",
            min_value=0.0,
            value=0.75,
            step=0.05,
            format="%.4f"
        )

    with col3:

        case_quantity = st.selectbox(
            "Quantità casse",
            [1, 10, 50, 100]
        )

    # CONVERSIONE TOKEN -> USD

    tokens_used = case_token_cost * case_quantity

    case_cost_usd = tokens_used * average_token_cost

    case_revenue = case_sell_price * case_quantity

    fee, net_revenue, profit, margin = calculate(
        case_cost_usd,
        case_revenue,
        fee_pct
    )

    st.markdown("### Risultato")

    a, b, c, d = st.columns(4)

    a.metric(
        "Token utilizzati",
        f"{tokens_used:,.2f}"
    )

    b.metric(
        "Costo reale in $",
        money(case_cost_usd)
    )

    c.metric(
        "Ricavo dopo commissione",
        money(net_revenue),
        delta=f"Fee: {money(fee)}"
    )

    d.metric(
        "Profitto netto",
        money(profit),
        delta=f"{margin:.2f}% sul costo"
    )

    st.info(
        f"{tokens_used:,.2f} token corrispondono a "
        f"{money(case_cost_usd)} di costo effettivo."
    )

    if owned_tokens > 0 and tokens_used > owned_tokens:

        st.warning(
            "Attenzione: i token necessari per questo acquisto "
            "superano il saldo indicato nel portafoglio."
        )

    # TABELLA QUANTITA

    st.markdown("### Confronto casse x1 / x10 / x50 / x100")

    case_rows = []

    for q in [1, 10, 50, 100]:

        tokens = case_token_cost * q

        cost = tokens * average_token_cost

        rev = case_sell_price * q

        f, net, p, m = calculate(
            cost,
            rev,
            fee_pct
        )

        case_rows.append({
            "Quantità": f"x{q}",
            "Token necessari": tokens,
            "Costo in $": cost,
            "Ricavo lordo": rev,
            "Commissione": f,
            "Ricavo dopo fee": net,
            "Profitto netto": p,
            "Margine": m
        })

    st.dataframe(
        pd.DataFrame(case_rows).style.format({
            "Token necessari": "{:,.2f}",
            "Costo in $": "${:.4f}",
            "Ricavo lordo": "${:.4f}",
            "Commissione": "${:.4f}",
            "Ricavo dopo fee": "${:.4f}",
            "Profitto netto": "${:.4f}",
            "Margine": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # PAREGGIO CASSE

    if average_token_cost > 0 and fee_pct < 100:

        break_even_case = (
            case_token_cost *
            average_token_cost /
            (1 - fee_pct / 100)
        )

        st.success(
            f"Prezzo minimo di vendita per cassa "
            f"per andare in pari: {money(break_even_case)}."
        )


# ==========================================
# TAB 3 - GUIDA
# ==========================================

with tab3:

    st.header("💡 Come funziona")

    st.markdown("""
    ### Acquisto token

    Inserisci quanto paghi per 1.000 token.
    Questo valore determina il costo dei token che rivendi.

    ### Portafoglio

    Inserisci quanti token possiedi e quanto hai speso
    complessivamente per acquistarli.

    Il costo medio del portafoglio viene calcolato così:

    `Spesa totale / Token posseduti`

    ### Casse

    Inserisci il costo della cassa in token e il prezzo
    di vendita in dollari.

    Il sistema converte automaticamente i token in dollari
    utilizzando il costo medio del portafoglio.

    ### Formula profitto netto

    `Ricavo vendita - Commissione - Costo token`

    **Nota:** il calcolo delle casse usa il costo medio
    dei token posseduti. Non viene scalato automaticamente
    il saldo dopo un acquisto.
    """)

st.divider()

st.caption(
    "Bloxstrike Profit Calculator · USD ($) · "
    "Commissione modificabile"
)
