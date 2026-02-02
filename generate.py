from predict import predict_outfit
from ontology import SUBTYPES
import itertools

shirts = ["white", "black", "beige"]
pants = ["black", "beige"]
shoes = ["black", "navy"]

results = []
style = "old_money"
shirt_st, pants_st, shoes_st = SUBTYPES["shirt"][0], SUBTYPES["pants"][0], SUBTYPES["shoes"][0]
fit, temp, occasion, outerwear = "regular", "mild", "business", "none"

for s, p, sh in itertools.product(shirts, pants, shoes):
    score = predict_outfit(s, p, sh, style, shirt_st, pants_st, shoes_st, fit, temp, occasion, outerwear)
    results.append((score, s, p, sh))

results.sort(reverse=True)

for r in results[:5]:
    print(r)
