import pytest

from prompts import wildcardmanager
from prompts.generators.randomprompt import RandomPromptGenerator


@pytest.fixture
def wildcard_manager():
    return wildcardmanager.WildcardManager(None)

@pytest.fixture
def seed():
    return 0

@pytest.fixture
def generator(wildcard_manager, seed):
    return RandomPromptGenerator(wildcard_manager, "A template", seed=seed)

class TestRandomPrompt:
    def test_simple_pick_variant(self, generator):
        template = "I love {bread|butter}"
        generator._template = template

        variant = generator.pick_variant(template)
        assert variant == "I love butter"

        variant = generator.pick_variant(template)
        assert variant == "I love butter"

        variant = generator.pick_variant(template)
        assert variant == "I love bread"

    def test_multiple_pick_variant(self, generator):
        template = "I love {2$$bread|butter}"
        generator._template = template

        variant = generator.pick_variant(template)
        assert variant == "I love butter, butter"

        variant = generator.pick_variant(template)
        assert variant == "I love bread, bread"

        variant = generator.pick_variant(template)
        assert variant == "I love butter, bread"

    def test_multiple_variant_one_option(self, generator):
        template = "I love {2$$bread}"
        generator._template = template

        variant = generator.pick_variant(template)
        assert variant == "I love bread, bread"

    def test_multiple_variant_zero_options(self, generator):
        template = "I love {}"
        generator._template = template

        variant = generator.pick_variant(template)
        assert variant == "I love "
