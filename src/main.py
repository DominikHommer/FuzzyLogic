from modules.fuzzy_controller import FuzzyController
from modules.fuzzy_rule import FuzzyRule
from modules.fuzzy_variable import FuzzyVariable
from modules.membership_function import MembershipFunction

mf_trap = lambda a, b, c, d: MembershipFunction(lambda x: 0.0 if x<=a or x>=d else ((x-a)/(b-a) if x<b else (1.0 if x<=c else (d-x)/(d-c))))
mf_tri  = lambda a, b, c: MembershipFunction(lambda x: 0.0 if x<=a or x>=c else ((x-a)/(b-a) if x<b else (c-x)/(c-b)))

health = FuzzyVariable('health', {
    'weak': mf_trap(0, 0, 30, 50),
    'medium': mf_tri(30, 50, 70),
    'strong': mf_trap(50, 70, 100, 100)
})
enemies = FuzzyVariable('enemies', {
    'low': mf_trap(0, 0, 25, 50),
    'mod': mf_tri(25, 50, 75),
    'high': mf_trap(50, 75, 100, 100)
})
distance = FuzzyVariable('distance', {
    'near': mf_trap(0, 0, 3, 6),
    'medium': mf_tri(3, 6, 9),
    'far': mf_trap(6, 9, 10, 10)
})

outlook = FuzzyVariable('outlook', {
    'poor': mf_trap(0, 0, 30, 50),
    'medium': mf_tri(30, 50, 70),
    'good': mf_trap(50, 70, 100, 100)
})

rules = []
labels = ['weak','medium','strong']
en_labels = ['low','mod','high']
dist_labels = ['near','medium','far']
for i, h in enumerate(labels):
    for j, e in enumerate(en_labels):
        for k, d in enumerate(dist_labels):
            if i + k - j > 1:
                out = 'good'
            elif i + k - j == 1:
                out = 'medium'
            else:
                out = 'poor'
            rules.append(FuzzyRule(
                [('health', h), ('enemies', e), ('distance', d)],
                ('outlook', out)
            ))

controller = FuzzyController(
    {'health': health, 'enemies': enemies, 'distance': distance},
    outlook,
    rules
)

if __name__ == '__main__':
    agg, ys = controller.infer({'health': 30, 'enemies': 90, 'distance': 8})
    print("Aggregated strengths:", agg)
    for method in ['min_of_max','max_of_max','mean_of_max','bisector','blend','centroid']:
        val = controller.defuzzify(ys, method)
        print(f"{method}: {val:.2f}")