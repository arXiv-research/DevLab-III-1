const dydxFlashloanerContract = new ethers.Contract(
  dydxFlashloanerAddress,
  def.abi,
  wallet
);

const main = async () => {
  const tx = await dydxFlashloanerContract.initiateFlashLoan(
    legos.dydx.soloMargin.address,
    legos.erc20.weth.address, // Wanna take out a WETH loan
    ethers.utils.parseEther("10"),      // Wanna loan 10 WETH
    {
      gasLimit: 6000000,
    }
  );
  await tx.wait();
};
