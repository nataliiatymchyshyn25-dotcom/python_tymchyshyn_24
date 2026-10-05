# Bracket Validator

A Python package for validating balanced brackets.

## Supported brackets

- `()`
- `{}`
- `<>`
- `[]`

## Usage

```python
from bracket_validator.bracket_validator import validate_brackets

validate_brackets("<div>{(test)}</div>")
```

If the brackets are balanced, the function completes without errors.

If the brackets are unbalanced, it raises `ValueError`:

```python
from bracket_validator.bracket_validator import validate_brackets

validate_brackets("text({")
```

Output:

```text
ValueError: Дужки незбалансовані на позиціях [4, 5]
text({
    ^^
```