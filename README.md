# Bloxstrike Profit Calculator

Webapp Streamlit per calcolare costi, ricavi, commissioni e profitti su token e casse Bloxstrike.

## Funzionalità
- Token: costo per 1.000 token configurabile, quantità 500/1.000/5.000/10.000 e prezzo di vendita per token.
- Prezzo iniziale di vendita token: $0.0045.
- Confronto tra prezzi di vendita alternativi.
- Casse: calcolo per x1/x10/x50/x100 con costo e prezzo di vendita unitari modificabili.
- Commissione configurabile (predefinita 15%).
- Calcolo profitto netto, margine e prezzo di pareggio.

## Avvio in locale
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Pubblicazione su Streamlit Community Cloud
1. Crea un repository GitHub **privato** e carica `app.py`, `requirements.txt`, `README.md` e `.gitignore`.
2. Apri https://share.streamlit.io/ e accedi con GitHub.
3. Seleziona **New app**, scegli il repository, il branch e `app.py`.
4. Seleziona **Deploy**.

Nota: prima di distribuire, verifica nelle impostazioni correnti di Streamlit Community Cloud che il piano e le autorizzazioni supportino il repository privato. Non inserire password o chiavi segrete nel codice.
