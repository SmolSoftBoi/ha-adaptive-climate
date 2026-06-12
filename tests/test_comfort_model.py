from comfort_model import ComfortCategory, ComfortInputs, calculate_adaptive_comfort


def test_calculates_default_adaptive_target():
    result = calculate_adaptive_comfort(
        ComfortInputs(indoor_temp=21.0, outdoor_temp=10.0)
    )

    assert result.target_temp == 21.4
    assert result.comfort_min == 18.4
    assert result.comfort_max == 24.4
    assert result.comfortable is True


def test_clamps_target_to_minimum():
    result = calculate_adaptive_comfort(
        ComfortInputs(indoor_temp=16.0, outdoor_temp=0.0, min_comfort_temp=18.0)
    )

    assert result.target_temp == 18.0
    assert "outside the normal adaptive-comfort range" in result.notes[0]


def test_category_i_has_narrower_band_than_category_iii():
    category_i = calculate_adaptive_comfort(
        ComfortInputs(indoor_temp=21.0, outdoor_temp=15.0, category=ComfortCategory.I)
    )
    category_iii = calculate_adaptive_comfort(
        ComfortInputs(indoor_temp=21.0, outdoor_temp=15.0, category=ComfortCategory.III)
    )

    assert category_i.comfort_max - category_i.comfort_min < category_iii.comfort_max - category_iii.comfort_min
