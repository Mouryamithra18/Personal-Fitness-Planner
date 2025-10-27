import sys
import os
import pytest

# Ensure repo root is importable for planner_utils
import sys, os
# ensure repo root on path so 'planner' package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from planner.planner_utils import generate_diet_plan


def test_generate_diet_plan_balanced():
    diet = generate_diet_plan('balanced', {}, 2000)
    assert diet['plan_type'] == 'balanced'
    assert diet['calories_target'] == 2000
    assert len(diet['meals']) == 7
    # Check structure of a day's meal
    day1 = diet['meals']['Day 1']
    assert isinstance(day1, list)
    assert 'meal' in day1[0] and 'cal' in day1[0] and 'suggestion' in day1[0]


@pytest.mark.parametrize('ptype,expected', [
    ('weight_loss', 'weight_loss'),
    ('strength', 'strength'),
    ('muscle_gain', 'muscle_gain')
])
def test_generate_diet_plan_types(ptype, expected):
    diet = generate_diet_plan(ptype, {}, 1800)
    assert diet['plan_type'] == expected
    assert all(isinstance(v, list) for v in diet['meals'].values())
