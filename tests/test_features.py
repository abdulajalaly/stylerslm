from stylerslm.features import INPUT_DIM, outfit_to_vector


def test_feature_vector_has_stable_dimension():
    vector = outfit_to_vector("white", "black", "brown", "formal", "oxford", "trousers", "loafers", "regular", "mild", "business", "none")
    assert len(vector) == INPUT_DIM
    assert sum(vector) == 11


def test_unknown_categories_are_encoded_as_zero():
    vector = outfit_to_vector("unknown", "black", "brown", "formal", "oxford", "trousers", "loafers", "regular", "mild", "business", "none")
    assert sum(vector) == 10