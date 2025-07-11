const contractAddress = '0xYourContractAddress';
const contractABI = [/* Your ABI here */];

let web3;
let contract;

window.addEventListener('load', async () => {
  if (window.ethereum) {
    web3 = new Web3(window.ethereum);
    await window.ethereum.request({ method: 'eth_requestAccounts' });
    contract = new web3.eth.Contract(contractABI, contractAddress);
  } else {
    alert('Please install MetaMask!');
  }
});

async function registerLandOnChain(owner, landId, location) {
  const accounts = await web3.eth.getAccounts();
  await contract.methods.registerLand(owner, landId, location)
    .send({ from: accounts[0] });
}
