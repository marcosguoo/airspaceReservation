async function main() {
    const AirspaceAuction = await ethers.getContractFactory("AirspaceAuction");
 
    // Start deployment, returning a promise that resolves to a contract object
    const airspace_reservation = await AirspaceAuction.deploy();   
    console.log("Contract deployed to address:", airspace_reservation.address);
 }
 
 main()
   .then(() => process.exit(0))
   .catch(error => {
     console.error(error);
     process.exit(1);
   });