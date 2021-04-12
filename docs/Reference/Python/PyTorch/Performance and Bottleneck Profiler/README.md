Profiling your training run can help you understand if there are any bottlenecks in your code.

Built-in checks
PyTorch Lightning supports profiling standard actions in the training loop out of the box, including:

on_epoch_start

on_epoch_end

on_batch_start

tbptt_split_batch

model_forward

model_backward

on_after_backward

optimizer_step

on_batch_end

training_step_end

on_training_end
