from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier

from model.config.core import config
from model.processing import features as pp

diabetes_pipe = Pipeline(
    [
        ("Red Neuronal",
            MLPClassifier(
                hidden_layer_sizes = config.model_config.hidden_layer_sizes,
                learning_rate_init = config.model_config.learning_rate_init, 
                max_iter = config.model_config.max_iter,
                random_state=config.model_config.model_random_state,
            ),
        ),
    ]
)
