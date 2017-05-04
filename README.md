# ross-django-utils
Some of the commonly-used utilities for Django Framework

## Installation

Install via `pip`:
```bash
pip install -e git+https://github.com/rossplt/ross-django-utils.git#egg=ross
```

In `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'ross',
    ...
]
```

## Usage

### `ross.core.models`
This contains some of the commonly-used abstract models when creating your own Models.

#### `ross.core.models.Timestamped`
Adds timestamping to your model - `created` and `updated` field. Sample usage:
```python
from ross.core.models import Timestamped

class MyModel(Timestamped):
    ...
    ...
```

#### `ross.core.models.Slugged`
Adds automatically-generated slug (on save) to a model - `slug` field. Sample usage:
```python
from ross.core.models import Slugged

class MyModel(Slugged):
    value_field_name = 'title'
    
    title = models.CharField('Title', max_length=200)
    ...
    ...
```
Note that the field defined by `value_field_name` must be added manually (it defaults to `title`). This configuration is necessary to tell the `Slugged` abstract model which field will be used as a base for slug generation. Slugs are always stored in `slug` field by default.
