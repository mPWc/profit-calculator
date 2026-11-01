
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
# FUNZIONE CALCOLO
# ==========================================

def calculate(cost, revenue, fee_pct):
    fee = revenue * fee_pct / 100
    net_revenue = revenue - fee
    profit = net_revenue - cost
    margin = profit / cost * 100 if cost > 0 else 0

    return fee, net_revenue, profit, margin


def money(value):
    return f"${value:,.4f}" if abs(value) < 1 else f"${value:,.2f}"


# ==========================================
# SIDEBAR - COMMISSIONI
# ==========================================

with st.sidebar:
    st.header("⚙️ Impostazioni")

    fee_pct = st.number_input(
        "Commissione sulle vendite (%)",
        min_value=0.0,
        max_value=100.0,
        value=15.0,
        step=0.5
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
# LOGICA ORIGINALE MANTENUTA
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
            format="%.4f",
            key="token_buy_1000"
        )

    with col2:
        sell_price = st.number_input(
            "Prezzo di vendita per token ($)",
            min_value=0.0,
            value=0.0045,
            step=0.0001,
            format="%.4f",
            key="token_sell_price"
        )

    quantity = st.selectbox(
        "Quantità token da calcolare",
        [500, 1000, 5000, 10000],
        key="token_quantity"
    )

    # COSTI E RICAVI TOKEN

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

    # CONFRONTO QUANTITA TOKEN

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

    # CONFRONTO PREZZI DI VENDITA

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
# NUOVA LOGICA INDIPENDENTE
# ==========================================

with tab2:

    st.header("📦 Calcolatore casse Bloxstrike")

    st.write(
        "Inserisci il costo dei token in dollari, "
        "il costo della cassa in token e il prezzo di vendita. "
        "Il calcolo del profitto sarà automatico."
    )

    st.markdown("### 1. Costo dei token")

    case_buy_1000 = st.number_input(
        "Quanto paghi in $ per 1.000 token?",
        min_value=0.0,
        value=2.50,
        step=0.05,
        format="%.4f",
        key="case_buy_1000"
    )

    st.caption(
        "Questo costo è indipendente dal prezzo inserito "
        "nella sezione Token."
    )

    st.markdown("### 2. Dati della cassa")

    col1, col2, col3 = st.columns(3)

    with col1:
        case_token_cost = st.number_input(
            "Costo di acquisto di 1 cassa (token)",
            min_value=0.0,
            value=42.0,
            step=1.0,
            key="case_token_cost"
        )

    with col2:
        case_sell_price = st.number_input(
            "Prezzo di vendita di 1 cassa ($)",
            min_value=0.0,
            value=0.21,
            step=0.01,
            format="%.4f",
            key="case_sell_price"
        )

    with col3:
        case_quantity = st.selectbox(
            "Quantità casse",
            [1, 10, 20, 50, 100],
            key="case_quantity"
        )

    # CALCOLO COSTO TOKEN PER CASSE

    cost_per_token = case_buy_1000 / 1000

    tokens_used = case_token_cost * case_quantity

    case_cost_usd = tokens_used * cost_per_token

    case_revenue = case_sell_price * case_quantity

    fee, net_revenue, profit, margin = calculate(
        case_cost_usd,
        case_revenue,
        fee_pct
    )

    st.markdown("### 3. Risultato")

    a, b, c, d = st.columns(4)

    a.metric(
        "Token utilizzati",
        f"{tokens_used:,.2f}"
    )

    b.metric(
        "Costo totale in $",
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
        f"Ogni cassa ti costa {money(case_token_cost * cost_per_token)} "
        f"in token. Dopo la commissione incassi "
        f"{money(case_sell_price * (1 - fee_pct / 100))} "
        f"per cassa."
    )

    # CONFRONTO QUANTITA CASSE

    st.markdown("### Confronto x1 / x10 / x50 / x100")

    case_rows = []

    for q in [1, 10, 20, 50, 100]:

        tokens = case_token_cost * q

        cost = tokens * cost_per_token

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

    # CONFRONTO COSTO TOKEN: 2.50, 3.00, 3.50 ECC.

    st.markdown("### Confronto: quanto cambia il profitto se cambia il costo dei token?")

    st.write(
        "Questa tabella mantiene invariati il costo della cassa "
        "e il prezzo di vendita, ma cambia il costo di acquisto "
        "dei 1.000 token."
    )

    comparison_prices = [2.00, 2.50, 3.00, 3.50, 4.00, 4.50, 5.00]

    comparison_rows = []

    for price in comparison_prices:

        cost_token = price / 1000

        total_cost = (
            case_token_cost *
            case_quantity *
            cost_token
        )

        f, net, p, m = calculate(
            total_cost,
            case_revenue,
            fee_pct
        )

        comparison_rows.append({
            "Costo per 1.000 token": price,
            "Costo totale casse": total_cost,
            "Ricavo dopo fee": net,
            "Profitto netto": p,
            "Margine": m
        })

    st.dataframe(
        pd.DataFrame(comparison_rows).style.format({
            "Costo per 1.000 token": "${:.2f}",
            "Costo totale casse": "${:.4f}",
            "Ricavo dopo fee": "${:.4f}",
            "Profitto netto": "${:.4f}",
            "Margine": "{:.2f}%"
        }),
        use_container_width=True,
        hide_index=True
    )

    # PREZZO DI PAREGGIO

    if fee_pct < 100:

        break_even_case = (
            case_token_cost *
            cost_per_token /
            (1 - fee_pct / 100)
        )

        st.success(
            f"Prezzo minimo di vendita per cassa "
            f"per non andare in perdita: "
            f"**{money(break_even_case)}**."
        )


# ==========================================
# TAB 3 - GUIDA
# ==========================================

with tab3:

    st.header("💡 Come funziona")

    st.markdown("""
    ### 🪙 Sezione Token

    Questa sezione calcola il profitto dalla rivendita dei token.

    Inserisci:
    - Quanto paghi per 1.000 token.
    - Il prezzo di vendita per singolo token.
    - La quantità che vuoi vendere.

    Il sistema calcola costo, ricavo, commissione e profitto netto.

    ### 📦 Sezione Casse

    Questa sezione ha un costo token indipendente.

    Inserisci:
    - Quanto paghi in dollari per 1.000 token.
    - Quanti token costa una cassa.
    - A quanto vendi una cassa.
    - Quante casse vuoi calcolare.

    Il costo della cassa viene convertito in dollari usando
    il prezzo di acquisto dei token inserito in questa sezione.

    ### Formula

    `Costo cassa = (Token per cassa / 1000) × Costo per 1000 token`

    `Profitto netto = Ricavo vendita - Commissione - Costo cassa`

    La commissione viene applicata sul ricavo di vendita.

    **Le due sezioni sono indipendenti:** modificare il costo
    dei token nella sezione Casse non cambia i calcoli della
    sezione Token.
    """)

st.divider()

st.caption(
    "Bloxstrike Profit Calculator · USD ($) · "
    "Commissione modificabile"
)
