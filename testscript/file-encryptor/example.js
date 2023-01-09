var encryptor = require('file-encryptor');

var key = 'My Super Secret Key';

// Encrypt file.
encryptor.encryptFile('input_file.txt', 'encrypted.dat', key, function(err) {
  // Encryption complete.
});

...

// Decrypt file.
encryptor.decryptFile('encrypted.dat', 'output_file.txt', key, function(err) {
  // Decryption complete.
});