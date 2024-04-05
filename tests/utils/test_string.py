from qrt.utils.string import camel_to_snake, snake_to_camel


def test_camel_to_snake():
    assert camel_to_snake("camelCase") == "camel_case"
    assert camel_to_snake("snake_case") == "snake_case"
    assert camel_to_snake("oneword") == "oneword"


def test_snake_to_camel():
    assert snake_to_camel("camelCase") == "camelCase"
    assert snake_to_camel("snake_case") == "snakeCase"
    assert snake_to_camel("oneword") == "oneword"
