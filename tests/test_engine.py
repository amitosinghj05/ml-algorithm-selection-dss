from dss.schemas import UserNeeds
from dss.knowledge_base import load_families
from dss.engine import rank_families


def test_tabular_finance_prefers_tree_ensembles():
    families = load_families("data/knowledge_base.yaml")
    needs = UserNeeds(
        domain="finance",
        modality="tabular",
        goal="classification",
        interpretability=False,
        privacy_sensitive=False,
        limited_labels=False,
        real_time=False
    )
    ranked = rank_families(needs, families)
    assert ranked[0][0].startswith("Tree Ensembles")


def test_image_healthcare_prefers_cnn_or_vit():
    families = load_families("data/knowledge_base.yaml")
    needs = UserNeeds(
        domain="healthcare",
        modality="image",
        goal="classification",
        interpretability=False,
        privacy_sensitive=True,   # adds some penalty to heavy compute, but should still rank vision families high
        limited_labels=True,
        real_time=False
    )
    ranked = rank_families(needs, families)
    top = ranked[0][0]
    assert ("CNNs" in top) or ("Vision Transformers" in top)


def test_privacy_sensitive_recommends_federated():
    families = load_families("data/knowledge_base.yaml")
    needs = UserNeeds(
        domain="healthcare",
        modality="tabular",
        goal="classification",
        interpretability=True,
        privacy_sensitive=True,
        limited_labels=False,
        real_time=False
    )
    ranked = rank_families(needs, families)
    names = [r[0] for r in ranked[:5]]
    assert any("Federated" in n for n in names)

