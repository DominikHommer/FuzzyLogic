import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

from modules.fuzzy_controller import FuzzyController
from modules.fuzzy_rule import FuzzyRule
from modules.fuzzy_variable import FuzzyVariable
from modules.membership_function import MembershipFunction


def trap_mf(a, b, c, d):
    def mf(x):
        if x <= a or x >= d: return 0.0
        if x < b: return (x - a) / (b - a)
        if x <= c: return 1.0
        return (d - x) / (d - c)
    return MembershipFunction(mf)

def tri_mf(a, b, c):
    def mf(x):
        if x <= a or x >= c: return 0.0
        if x < b: return (x - a) / (b - a)
        return (c - x) / (c - b)
    return MembershipFunction(mf)

def bell_mf(a, b, c):
    def mf(x):
        return 1.0 / (1.0 + (((x - c) / a) ** (2 * b)))
    return MembershipFunction(mf)


# Fuzzy variables setup
health = FuzzyVariable('Health', {
    'weak': trap_mf(0, 0, 30, 50),
    'medium': tri_mf(30, 50, 70),
    'strong': trap_mf(50, 70, 100, 100)
}, domain=(0, 100))

enemies = FuzzyVariable('Enemies', {
    'low': trap_mf(0, 0, 25, 50),
    'mod': tri_mf(25, 50, 75),
    'high': trap_mf(50, 75, 100, 100)
}, domain=(0, 100))

distance = FuzzyVariable('Distance', {
    'near': trap_mf(0, 0, 3, 6),
    'medium': tri_mf(3, 6, 9),
    'far': trap_mf(6, 9, 10, 10)
}, domain=(0, 10))

outlook = FuzzyVariable('Outlook', {
    'poor': trap_mf(0, 0, 30, 50),
    'medium': tri_mf(30, 50, 70),
    'good': trap_mf(50, 70, 100, 100)
}, domain=(0, 100))


labels = ['weak', 'medium', 'strong']
e_labels = ['low', 'mod', 'high']
d_labels = ['near', 'medium', 'far']
rules = []

for i, h in enumerate(labels):
    for j, e in enumerate(e_labels):
        for k, d in enumerate(d_labels):
            score = i + k - j
            out = 'good' if score > 1 else 'medium' if score == 1 else 'poor'
            rules.append(FuzzyRule(
                [('Health', h), ('Enemies', e), ('Distance', d)],
                ('Outlook', out)
            ))

controller = FuzzyController(
    {'Health': health, 'Enemies': enemies, 'Distance': distance},
    outlook,
    rules
)

st.set_page_config(layout="wide")
st.title('Fuzzy-Logic Game AI Controller')

with st.sidebar:
    g_health = st.slider('Health', 0, 100, 30)
    g_enemies = st.slider('Enemy Count', 0, 100, 90)
    g_distance = st.slider('Distance', 0.0, 10.0, 8.0, 0.1)
    method = st.selectbox(
        'Defuzzification Method',
        ['min_of_max', 'max_of_max', 'mean_of_max', 'bisector', 'blend', 'centroid']
    )

fuzzified, agg, ys = controller.infer({
    'Health': g_health,
    'Enemies': g_enemies,
    'Distance': g_distance
})
def_val = controller.defuzzify(ys, method)

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

st.markdown('---')
c1, c2 = st.columns(2)
with c1:
    st.subheader("Aggregated Strengths")
    st.write(agg)
with c2:
    st.subheader("Crisp Command")
    cmd = 'ANGRIFF' if def_val >= 66 else 'VERTEIDIGUNG' if def_val >= 34 else 'RÜCKZUG'
    st.success(cmd)
