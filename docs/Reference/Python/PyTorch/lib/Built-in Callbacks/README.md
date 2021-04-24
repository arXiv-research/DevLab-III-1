Lightning has a few built-in callbacks.

NOTE

For a richer collection of callbacks, check out our bolts library.

BackboneFinetuning

Finetune a backbone model based on a learning rate user-defined scheduling.

BaseFinetuning

This class implements the base logic for writing your own Finetuning Callback.

Callback

Abstract base class used to build new callbacks.

EarlyStopping

Monitor a metric and stop training when it stops improving.

GPUStatsMonitor

Automatically monitors and logs GPU stats during training stage.

GradientAccumulationScheduler

Change gradient accumulation factor according to scheduling.

LambdaCallback

Create a simple callback on the fly using lambda functions.

LearningRateMonitor

Automatically monitor and logs learning rate for learning rate schedulers during training.

ModelCheckpoint

Save the model after every epoch by monitoring a quantity.

ModelPruning

Model pruning Callback, using PyTorch’s prune utilities.

ProgressBar

This is the default progress bar used by Lightning.

ProgressBarBase

The base class for progress bars in Lightning.

QuantizationAwareTraining

Quantization allows speeding up inference and decreasing memory requirements by performing computations and storing tensors at lower bitwidths (such as INT8 or FLOAT16) than floating point precision.

StochasticWeightAveraging

Implements the Stochastic Weight Averaging (SWA) Callback to average a model.

Persisting State
Some callbacks require internal state in order to function properly. You can optionally choose to persist your callback’s state as part of model checkpoint files using the callback hooks on_save_checkpoint() and on_load_checkpoint(). However, you must follow two constraints:

Your returned state must be able to be pickled.

You can only use one instance of that class in the Trainer callbacks list. We don’t support persisting state for multiple callbacks of the same class.

Best Practices
The following are best practices when using/designing callbacks.

Callbacks should be isolated in their functionality.

Your callback should not rely on the behavior of other callbacks in order to work properly.

Do not manually call methods from the callback.

Directly calling methods (eg. on_validation_end) is strongly discouraged.

Whenever possible, your callbacks should not depend on the order in which they are executed.

