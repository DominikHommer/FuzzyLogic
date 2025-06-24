"""
Hilfsfunktionen für das Streamlit-UI:
- Ermöglicht das flexible Editieren und Erstellen von Membership Functions durch den Nutzer.
"""

import streamlit as st
from config import MF_TYPES, MF_PARAM_HELP
from modules.fuzzy_logic.fuzzy_variable import FuzzyVariable

def mf_params_ui(var, label, mf_type, params):
    """
    Erstellt für einen MF-Typ die passenden Number-Inputs in Streamlit.

    Args:
        var (str): Name der Variable, z.B. 'Health'
        label (str): Label der MF, z.B. 'weak'
        mf_type (str): Typ der MF, z.B. 'Trapezoid'
        params (list): Default-Parameterwerte

    Returns:
        list: Vom User gewählte Parameterwerte
    """
    param_names = MF_TYPES[mf_type]["params"]
    cols = st.columns(len(param_names))
    vals = []
    for i, pname in enumerate(param_names):
        help_text = MF_PARAM_HELP.get(mf_type, {}).get(pname, "")
        min_value = 0.01 if mf_type == "Bell" and pname == "a" else None
        val = cols[i].number_input(
            pname,
            value=float(params[i]),
            min_value=min_value,
            key=f"{var}_{label}_{mf_type}_{pname}",
            help=help_text
        )
        vals.append(val)
    return vals

def build_var_from_ui(varname, config):
    """
    Baut eine FuzzyVariable durch UI-Eingabe in Streamlit zusammen.

    Args:
        varname (str): Name der Fuzzy-Variable (z.B. 'Health')
        config (dict): Konfiguration der Variable aus VAR_CONFIG

    Returns:
        FuzzyVariable: Das per UI erzeugte Objekt mit allen zugehörigen Membership Functions
    """
    terms = {}
    with st.expander(f"{varname} Membership Functions", expanded=False):
        tab_objs = st.tabs(config["labels"])
        for tab, label in zip(tab_objs, config["labels"]):
            with tab:
                default_type, default_vals = config["defaults"][label]
                mf_type = st.selectbox(
                    "Typ",
                    MF_TYPES.keys(),
                    index=list(MF_TYPES).index(default_type),
                    key=f"{varname}_{label}_type"
                )
                default = default_vals if mf_type == default_type else MF_TYPES[mf_type]["default"]
                vals = mf_params_ui(varname, label, mf_type, default)
                mf_func = MF_TYPES[mf_type]["func"]
                terms[label] = mf_func(*vals)
    return FuzzyVariable(varname, terms, domain=config["domain"])
