PyTorch 1.8.1 Release Notes

New Features
Improvements
Bug Fixes
Documentation

New Features
Enable use of autocast for pytorch xla (#48570)

Improvements

Make torch. submodule import more autocomplete-friendly (#52339)
Add support in ONNX for torch.{isinf,any,all} (#53529)
Replace thrust with cub in GPU implementation of torch.randperm for performance (#54537)

Bug fixes

Misc
Fixes for torch.distributions validation checks (#53763/issues/53763))

Allow changing the padding vector for nn.Embedding (#53447)

Fix TensorPipe for large copies and interoperability with CUDA (#53804)

Properly de-sugar Ellipsis in TorchScript (#53766)

Stop using OneDNN for group convolutions when groups size is a multiple of 24 (#54015)

Use int8_t instead of char in {load,store}_scalar (#52616)

Make ideep honor torch.set_num_thread (#53871)

Fix dimension out of range in pixel_{un}shuffle (#54178)

Update kineto to fix libtorch builds (#54205)

Fix distributed autograd CUDA stream synchronization for send/recv operations (#54358)

ONNX
Update error handling in ONNX to avoid ValueError (#53548)
Update assign output shape for nested structure and dict output (#53311)
Update embedding export wrt padding_idx (#53931)

Documentation
Doc update for torch.fx (#53674)
Fix distributed.rpc.options.TensorPipeRpcBackendOptions.set_device_map (#53508)
Update example for nn.LSTMCell (#51983)
Update doc for the padding_idx argument for nn.Embedding (#53809)
Update general doc template (#54141)

Source: README.md, updated 2021-03-24  uploaded on 2021-04-26
