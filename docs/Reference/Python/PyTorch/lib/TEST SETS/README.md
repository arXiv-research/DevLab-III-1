Lightning forces the user to run the test set separately to make sure it isn’t evaluated by mistake. Testing is performed using the trainer object’s .test() method.

Trainer.test(model=None, test_dataloaders=None, ckpt_path='best', verbose=True, datamodule=None)[SOURCE]
Perform one evaluation epoch over the test set. It’s separated from fit to make sure you never run on your test set until you want to.

Parameters
model (Optional[LightningModule]) – The model to test.

test_dataloaders (Union[DataLoader, List[DataLoader], None]) – Either a single PyTorch DataLoader or a list of them, specifying test samples.

ckpt_path (Optional[str]) – Either best or path to the checkpoint you wish to test. If None, use the current weights of the model. When the model is given as argument, this parameter will not apply.

verbose (bool) – If True, prints the test results.

datamodule (Optional[LightningDataModule]) – A instance of LightningDataModule.

Returns
Returns a list of dictionaries, one for each test dataloader containing their respective metrics.
