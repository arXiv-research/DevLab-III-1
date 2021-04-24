class MyDataModule(pl.LightningDataModule):
    ...
    def test_dataloader(self):
        return DataLoader(...)

# setup your datamodule
dm = MyDataModule(...)

# test (pass in datamodule)
trainer.test(datamodule=dm)
