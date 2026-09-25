"""Reusable E6 data API with lazy imports."""
__all__ = ['load_rows', 'model_inputs', 'training_examples', 'score', 'validate']
def __getattr__(name):
    if name not in __all__: raise AttributeError(name)
    from . import dataset
    return getattr(dataset, name)
