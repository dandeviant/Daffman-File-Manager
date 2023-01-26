// Init aesCrypt library
const aes = aesCrypt;

let fileSecret = document.getElementById("fileSecret").files[0];

let password = "foopassword"

// encryption/decryption

// encrypt typed array (Uint8Array)
aes.encrypt(fileSecret, password).then((encrypted) => {
  console.log(encrypted);
});

let fileEncrypted = document.getElementById("fileEncrypted").files[0];

// decrypt typed array (Uint8Array)
aes.decrypt(fileEncrypted, password).then((decrypted) => {

  // transform Uint8Array to Latin1 string
  let secret = aes.utils.bytes2str(decrypted);
  
  console.log(secret);
});