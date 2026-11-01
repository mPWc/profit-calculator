
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Bloxstrike Profit Calculator",
    page_icon="💰",
    layout="wide"
)

# -----------------------------
# STILE
# -----------------------------

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
st.caption("Token, casse, commissioni e profitto netto.")

# -----------------------------
# FUNZIONI
# -----------------------------

def money(value):
    return f"${value:,.4f}" if abs(value) < 1 else f"${value:,.2f}"


def calculate(cost, revenue, fee_pct):
    fee = revenue * fee_pct / 100
    net_revenue = revenue - fee
    profit = net_revenue - cost

    margin = (
        profit / cost * 100
        if cost > 0 else 0
    )

    return fee, net_revenue, profit, margin


# -----------------------------
# SIDEBAR: PORTAFOGLIO
# -----------------------------

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

    fee_pct = st.number_input(
        "Commissione sulle vendite (%)",
        min_value=0.0,
        max_value=100.0,
        value=15.0,
        step=0.5
    )


# -----------------------------
# COSTO MEDIO TOKEN
# -----------------------------

average_token_cost = (
    total_spent / owned_tokens
    if owned_tokens > 0 else 0
)

cost_per_1000 = average_token_cost * 1000

st.subheader("📊 Riepilogo portafoglio")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Token disponibili",
    f"{owned_tokens:,.0f}"
)

col2.metric(
    "Spesa totale",
    money(total_spent)
)

col3.metric(
    "Costo per 1.000 token",
    money(cost_per_1000)
)

if owned_tokens == 0:
    st.warning(
        "Inserisci il numero di token posseduti "
        "nella barra laterale."
    )

# -----------------------------
# TABS
# -----------------------------

tab_tokens, tab_cases, tab_guide = st.tabs([
    "🪙 Token",
    "📦 Casse Bloxstrike",
    "💡 Guida"
])


# =================================================
# TAB 1: TOKEN
# =================================================

with tab_tokens:

    st.subheader("🪙 Calcolatore token")

    st.write(
        "Calcola il profitto dalla vendita dei tuoi token."
    )

    col1, col2 = st.columns(2)

    with col1:

        token_quantity = st.selectbox(
            "Quantità token",
            [500, 1000, 5000, 10000]
        )

    with col2:

        token_sell_price = st.number_input(
            "Prezzo di vendita per token ($)",
            min_value=0.0,
            value=0.0045,
            step=0.0001,
            format="%.4f"
        )

    token_cost = average_token_cost * token_quantity

    token_revenue = token_sell_price * token_quantity

    fee, net_revenue, profit, margin = calculate(
        token_cost,
        token_revenue,
        fee_pct
    )

    st.markdown("### Risultati")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Costo token", money(token_cost))
    c2.metric("Ricavo lordo", money(token_revenue))
    c3.metric("Commissione", money(fee))
    c4.metric(
        "Profitto netto",
        money(profit),
        delta=f"{margin:.2f}% sul costo"
    )

    st.info(
        f"Ricavo dopo commissione: **{money(net_revenue)}**"
    )

    st.markdown("### Confronto prezzi di vendita")

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

    rows = []

    for price in prices:

        revenue = price * token_quantity

        f, net, p, m = calculate(
            token_cost,
            revenue,
            fee_pct
        )

        rows.append({
            "Prezzo/token": price,
            "Ricavo lordo": revenue,
            "Commissione": f,
            "Ricavo dopo fee": net,
            "Profitto netto": p,
            "Margine": m
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df.style.format({
            "Prezzo/token": "${:.4f}",
            "Ricavo lordo": "${:.4f}",
            "Commissione": "${:.4f}",
            "Ricavo dopo fee": "${:.4f}",
            "Profitto netto": "${:.4f}",
            "Margine": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    if owned_tokens > 0 and fee_pct < 100:

        break_even = (
            average_token_cost /
            (1 - fee_pct / 100)
        )

        st.success(
            f"Prezzo minimo di pareggio: "
            f"**${break_even:.6f} per token**"
        )


# =================================================
# TAB 2: CASSE
# =================================================

with tab_cases:

    st.subheader("📦 Calcolatore casse Bloxstrike")

    st.write(
        "Il costo di acquisto delle casse è espresso "
        "in TOKEN. Il sistema converte automaticamente "
        "il costo in dollari usando il tuo portafoglio."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        case_token_price = st.number_input(
            "Costo acquisto di 1 cassa (token)",
            min_value=0.0,
            value=100.0,
            step=10.0
        )

    with col2:

        case_sell_price = st.number_input(
            "Prezzo vendita di 1 cassa ($)",
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

    # CALCOLO COSTI

    tokens_required = (
        case_token_price * case_quantity
    )

    case_cost_usd = (
        tokens_required * average_token_cost
    )

    case_revenue = (
        case_sell_price * case_quantity
    )

    fee, net_revenue, profit, margin = calculate(
        case_cost_usd,
        case_revenue,
        fee_pct
    )

    # RISULTATI

    st.markdown("### Risultati")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Costo totale in token",
        f"{tokens_required:,.2f}"
    )

    c2.metric(
        "Costo reale in $",
        money(case_cost_usd)
    )

    c3.metric(
        "Ricavo dopo commissione",
        money(net_revenue),
        delta=f"Fee: {money(fee)}"
    )

    c4.metric(
        "Profitto netto",
        money(profit),
        delta=f"{margin:.2f}% sul costo"
    )

    st.info(
        f"Stai utilizzando **{tokens_required:,.2f} token**, "
        f"che al tuo costo medio equivalgono a "
        f"**{money(case_cost_usd)}**."
    )

    # CONFRONTO QUANTITA

    st.markdown("### Confronto x1 / x10 / x50 / x100")

    rows = []

    for quantity in [1, 10, 50, 100]:

        tokens = case_token_price * quantity

        cost_usd = tokens * average_token_cost

        revenue = case_sell_price * quantity

        f, net, p, m = calculate(
            cost_usd,
            revenue,
            fee_pct
        )

        rows.append({
            "Quantità": f"x{quantity}",
            "Token necessari": tokens,
            "Costo in $": cost_usd,
            "Ricavo lordo": revenue,
            "Commissione": f,
            "Ricavo dopo fee": net,
            "Profitto netto": p,
            "Margine": m
        })

    df = pd.DataFrame(rows)

    st.dataframe(
        df.style.format({
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

    # PAREGGIO

    if average_token_cost > 0 and fee_pct < 100:

        break_even_case = (
            case_token_price *
            average_token_cost /
            (1 - fee_pct / 100)
        )

        st.success(
            f"Prezzo minimo di vendita per cassa "
            f"per andare in pari: "
            f"**{money(break_even_case)}**"
        )


# =================================================
# TAB 3: GUIDA
# =================================================

with tab_guide:

    st.subheader("💡 Come funziona il calcolatore")

    st.markdown("""
    **1. Portafoglio token**

    Inserisci quanti token possiedi e quanto hai speso
    complessivamente per acquistarli.

    **2. Costo medio**

    Il sistema calcola automaticamente:

    `Spesa totale / Token posseduti`

    **3. Acquisto casse**

    Inserisci quanti token costa una singola cassa.

    **4. Conversione in dollari**

    Il costo della cassa viene convertito utilizzando
    il costo medio effettivo dei tuoi token.

    **5. Vendita e profitto**

    Il profitto viene calcolato sottraendo:
    - Il costo reale dei token utilizzati.
    - La commissione sulla vendita.
    - Dal ricavo lordo della vendita.

    **Formula:**

    `Profitto = Ricavo vendita - Fee - Costo token`

    Nota: viene utilizzato il costo medio complessivo
    dei token, anche se acquistati in momenti diversi.
    """)

st.divider()

st.caption(
    "Bloxstrike Profit Calculator · USD ($) · "
    "Commissioni configurabili"
)
