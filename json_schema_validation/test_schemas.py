import json
from pathlib import Path

import jsonschema
import pytest

_schemas_path = Path(__file__).parent / "schemas"


def _get_schema(name):
    with open(_schemas_path / f"{name}.json") as schema_file:
        return json.load(schema_file)


def _json_data(value):
    return {"field": value}


class TestDateTime:
    @pytest.fixture
    def schema(self):
        return _get_schema("date_schema")

    @pytest.mark.parametrize("value", ["2018-06-19"])
    def test__valid_validation(self, schema, value):
        jsonschema.validate(
            _json_data(value), schema, format_checker=jsonschema.FormatChecker()
        )

    @pytest.mark.parametrize(
        "value", ["20070619", "not a date", None, 0, 0.0, False, {}, []]
    )
    def test__invalid_validation(self, schema, value):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(
                _json_data(value), schema, format_checker=jsonschema.FormatChecker()
            )


class TestEnum:
    @pytest.fixture
    def schema(self):
        return _get_schema("enum_schema")

    @pytest.mark.parametrize("value", ["A", "B", "C"])
    def test__valid_validation(self, schema, value):
        jsonschema.validate(
            _json_data(value), schema, format_checker=jsonschema.FormatChecker()
        )

    @pytest.mark.parametrize("value", ["Z", None, 0, 0.0, False, {}, []])
    def test__invalid_validation(self, schema, value):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(
                _json_data(value), schema, format_checker=jsonschema.FormatChecker()
            )


class TestInteger:
    @pytest.fixture
    def schema(self):
        return _get_schema("int_schema")

    @pytest.mark.parametrize("value", [1, 2, 3, 0, 1.0, 1.0000])
    def test__valid_validation(self, schema, value):
        jsonschema.validate(
            _json_data(value), schema, format_checker=jsonschema.FormatChecker()
        )

    @pytest.mark.parametrize("value", ["A", "Z", None, 15.5, False, {}, []])
    def test__invalid_validation(self, schema, value):
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(
                _json_data(value), schema, format_checker=jsonschema.FormatChecker()
            )
