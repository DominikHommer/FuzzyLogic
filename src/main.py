import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from modules.fuzzy_logic.fuzzy_rule import FuzzyRule
from modules.fuzzy_logic.fuzzy_controller import FuzzyController
from utils.ui_helper import build_var_from_ui
from config import VAR_CONFIG

# -------------------------------
# Streamlit App Setup & Inputs
# -------------------------------

st.set_page_config(layout="wide")
st.title('Fuzzy-Logic Game AI Controller')

# --- Sidebar: Inputwerte für das Fuzzy-System
with st.sidebar:
    st.header("Inputwerte")
    g_health = st.slider('Health', 0, 100, 30, 1)
    g_enemies = st.slider('Enemy Count', 0, 100, 90, 1)
    g_distance = st.slider('Distance', 0.0, 10.0, 8.0, 0.1)
    method = st.selectbox(
        'Defuzzification Method',
        ['min_of_max', 'max_of_max', 'mean_of_max', 'centroid']
    )

# -----------------------------------------
# Membership Functions für alle Variablen
# -----------------------------------------

st.header("Wähle Membership Functions")
cols = st.columns(2)
with cols[0]:
    health = build_var_from_ui("Health", VAR_CONFIG["Health"])
    enemies = build_var_from_ui("Enemies", VAR_CONFIG["Enemies"])
with cols[1]:
    distance = build_var_from_ui("Distance", VAR_CONFIG["Distance"])
    outlook = build_var_from_ui("Outlook", VAR_CONFIG["Outlook"])

# -----------------------------------------
# Fuzzy-Regel-Editor (Regeln anpassen)
# -----------------------------------------

st.header("Fuzzy-Regel-Editor")

# Session-State für Regeln initialisieren (nur beim ersten Laden)
if "rules" not in st.session_state:
    st.session_state.rules = [
        # Beispiel-Regeln (Initial-Set)
        ({"Health": "strong", "Enemies": "low"}, ("Outlook", "good")),
        ({"Health": "strong", "Enemies": "mod"}, ("Outlook", "good")),
        ({"Health": "strong", "Enemies": "high"}, ("Outlook", "medium")),
        ({"Health": "medium", "Enemies": "low"}, ("Outlook", "good")),
        ({"Health": "medium", "Enemies": "mod"}, ("Outlook", "medium")),
        ({"Health": "medium", "Enemies": "high"}, ("Outlook", "poor")),
        ({"Health": "weak", "Enemies": "low"}, ("Outlook", "medium")),
        ({"Health": "weak", "Enemies": "mod"}, ("Outlook", "poor")),
        ({"Health": "weak", "Enemies": "high"}, ("Outlook", "poor")),
        ({"Distance": "near", "Enemies": "low"}, ("Outlook", "good")),
        ({"Distance": "near", "Enemies": "mod"}, ("Outlook", "good")),
        ({"Distance": "near", "Enemies": "high"}, ("Outlook", "medium")),
        ({"Distance": "medium", "Enemies": "low"}, ("Outlook", "good")),
        ({"Distance": "medium", "Enemies": "mod"}, ("Outlook", "medium")),
        ({"Distance": "medium", "Enemies": "high"}, ("Outlook", "poor")),
        ({"Distance": "far", "Enemies": "low"}, ("Outlook", "medium")),
        ({"Distance": "far", "Enemies": "mod"}, ("Outlook", "poor")),
        ({"Distance": "far", "Enemies": "high"}, ("Outlook", "poor")),
    ]

# --- UI für das Hinzufügen neuer Regeln ---
with st.expander("Neue Regel hinzufügen", expanded=False):
    with st.form("add_rule_form", clear_on_submit=True):
        st.write("Wenn ...")
        antecedents = {}
        all_input_vars = ["Health", "Enemies", "Distance"]
        # Für jede Input-Variable kann eine Bedingung gesetzt werden, oder 'keine Bedingung'
        for var in all_input_vars:
            label = st.selectbox(
                f"{var} ist ...",
                ["- (keine Bedingung) -"] + VAR_CONFIG[var]["labels"],
                key=f"rule_add_{var}"
            )
            antecedents[var] = None if label.startswith("-") else label

        st.write("Dann ...")
        out_label = st.selectbox(
            f"Outlook ist ...",
            VAR_CONFIG["Outlook"]["labels"],
            key="rule_add_out"
        )
        submitted = st.form_submit_button("Regel hinzufügen")
        if submitted:
            # Regel nur anlegen, wenn mindestens eine Bedingung gesetzt ist und es noch kein Duplikat gibt
            rule_ante = {k: v for k, v in antecedents.items() if v is not None}
            if not rule_ante:
                st.warning("Mindestens eine Bedingung muss gewählt werden!")
            else:
                rule_cons = ("Outlook", out_label)
                exists = any(
                    (old_cons == rule_cons and old_ante == rule_ante)
                    for old_ante, old_cons in st.session_state.rules
                )
                if exists:
                    st.warning("Diese Regel existiert bereits!")
                else:
                    st.session_state.rules.append((rule_ante, rule_cons))
                    st.success("Regel hinzugefügt!")

# --- Aktuelles Regel-Set anzeigen und Regeln löschen ---
with st.expander("Aktuelles Regel-Set", expanded=False):
    for i, (conds, cons) in enumerate(st.session_state.rules):
        cond_str = " & ".join([f"{k}={v}" for k, v in conds.items()])
        rule_str = f"{cond_str} → {cons[0]}={cons[1]}"
        col1, col2 = st.columns([8, 1])
        col1.markdown(rule_str)
        # Löscht die entsprechende Regel und refresht das UI
        if col2.button("Löschen", key=f"del_rule_{i}"):
            st.session_state.rules.pop(i)
            st.rerun()

# -----------------------------------------
# Regel-Liste in FuzzyRule-Objekte umwandeln
# -----------------------------------------

custom_rules = []
for conds, cons in st.session_state.rules:
    antecedents = [(k, v) for k, v in conds.items()]
    custom_rules.append(FuzzyRule(antecedents, cons))

# -----------------------------------------
# Fuzzy Inferenz und Defuzzifizierung
# -----------------------------------------

controller = FuzzyController(
    {'Health': health, 'Enemies': enemies, 'Distance': distance},
    outlook,
    custom_rules
)

fuzzified, agg, ys = controller.infer({
    'Health': g_health,
    'Enemies': g_enemies,
    'Distance': g_distance
})
def_val = controller.defuzzify(ys, method)

# -----------------------------------------
# Visualisierungen (MFs, Regeln, Output)
# -----------------------------------------

# --- Input Membership Functions ---
cols = st.columns(3)
for col, (var, val) in zip(cols, [('Health', g_health), ('Enemies', g_enemies), ('Distance', g_distance)]):
    fv = controller.input_vars[var]
    xs = np.linspace(fv.domain[0], fv.domain[1], 400)
    fig, ax = plt.subplots(figsize=(3, 2.5))
    for lbl, mf in fv.terms.items():
        ys_mf = np.array([mf(x) for x in xs])
        ax.plot(xs[ys_mf > 0], ys_mf[ys_mf > 0], label=lbl)
    ax.axvline(val, color='k', linestyle='--')
    ax.set_title(var)
    ax.set_ylim(0, 1)
    ax.set_ylabel('μ')
    ax.legend(fontsize='x-small')
    col.pyplot(fig)

# --- Regelaktivierungen: Geclippte Output Sets ---
st.header("Rule-level Clipped Output Sets")
color_map = {'poor': 'salmon', 'medium': 'gold', 'good': 'lightgreen'}
fired = [(r, r.evaluate(fuzzified)) for r in controller.rules]
fired = [(r, a) for r, a in fired if a > 0]
cols_r = st.columns(len(fired) or 1)
for col, (rule, alpha) in zip(cols_r, fired):
    term = rule.consequent[1]
    fig_r, ax_r = plt.subplots(figsize=(2, 2))
    xs_o = controller.xs
    ys_clip = np.minimum(alpha, np.array([outlook.terms[term](x) for x in xs_o]))
    ax_r.fill_between(xs_o, ys_clip, color=color_map[term], alpha=0.6)
    ax_r.set_title(f"{term}\nα={alpha:.2f}", fontsize=8)
    ax_r.set_ylim(0, 1)
    ax_r.set_xticks([])
    ax_r.set_yticks([])
    col.pyplot(fig_r)

# --- Output MF (ungewichtet) ---
st.header("Raw Output Membership Functions")
xs_out = np.linspace(outlook.domain[0], outlook.domain[1], 400)
fig_mf, ax_mf = plt.subplots(figsize=(6, 2.5))
for lbl, mf in outlook.terms.items():
    ys_mf = np.array([mf(x) for x in xs_out])
    ax_mf.plot(xs_out[ys_mf > 0], ys_mf[ys_mf > 0], label=lbl)
ax_mf.set_ylim(0, 1)
ax_mf.set_ylabel('μ')
ax_mf.legend(fontsize='small')
st.pyplot(fig_mf)

# --- Aggregierte Ausgabe & Defuzzifizierung ---
st.header("Aggregated Output & Defuzzification")
fig_out, ax_out = plt.subplots(figsize=(6, 2.5))
for term, degree in agg.items():
    ys_term = np.minimum(degree, np.array([outlook.terms[term](x) for x in controller.xs]))
    ax_out.fill_between(controller.xs, ys_term, color=color_map[term], alpha=0.4,
                        label=f"{term} (α={degree:.2f})")
ax_out.plot(controller.xs, ys, color='k', linewidth=1)
ax_out.axvline(def_val, color='r', linestyle='--', label=f"Defuzz = {def_val:.2f}")
ax_out.set_ylim(0, 1)
ax_out.set_ylabel('μ')
ax_out.set_xlabel('Outlook')
ax_out.legend(fontsize='small')
st.pyplot(fig_out)

# --- Ausgabe: Stärken & Crisp-Command ---
st.markdown('---')
c1, c2 = st.columns(2)
with c1:
    st.subheader("Aggregated Strengths")
    st.write(agg)
with c2:
    st.subheader("Crisp Command")
    # Definierte Schwellenwerte für Ausgabekommandos
    cmd = 'ANGRIFF' if def_val >= 66 else 'VERTEIDIGUNG' if def_val >= 34 else 'RÜCKZUG'
    st.success(cmd)
