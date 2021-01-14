import os.path
from Block import Block
from Certificate import Certificate

# define Blockchain
class Blockchain:
  def __init__(self, isNew, file):
    self.chain = []
    self.file = file
    if isNew:
      # Reset block chain, starts from genesis block
      genesis_block = Block.create_genesis_block()
      self.chain.append(genesis_block)
      self.previous_block = self.chain[0]
      f = open(self.file, "w")
      f.write(str(genesis_block) + "\n")
      f.close()
      print("Blockchain data reset successfully!")
    else:
      # get blockchain from file
      self.get_blockchain_from_file()
      self.previous_block = self.chain[len(self.chain)-1]
      print("Blockchain data loaded successfully (" + str(len(self.chain)) + " blocks)!")

  # output the len of the blockchain
  def __len__(self):
    return len(self.chain)

  # to string method to print blockchain
  def __str__(self):
    s = ""
    for x in self.chain:
      s+= "\nBlock " + str(x) + "\n"
    return s
  
  # generate blockchain from textfile (get data by line)
  def get_blockchain_from_file(self):
    if os.path.isfile(self.file):
      f = open(self.file, "r")
      for x in f:
        items = x.strip().split(" *** ")
        current_block = Block(int(items[0]), items[1], items[2], items[3])
        current_block.set_hash(items[4])
        self.chain.append(current_block)
      f.close()

  # Add new block to blockchain
  def add_block(self, data):
    print("Adding block to blockchain...")
    block_to_add = Block.create_next_block(self.previous_block, str(data))
    self.chain.append(block_to_add)
    f = open(self.file, "a")
    f.write(str(block_to_add) + "\n")
    f.close()
    self.previous_block = block_to_add
    print("Block added successfully to blockchain!")
    print("Block detail: ")
    print(str(block_to_add))
  
  # validate blockchain (check if block hash is valid + check if current hash match with the previous hash of next block)
  def validate_blockchain(self):
    s = ""
    for i in range(0, len(self.chain) - 1):
      if not self.chain[i].validate_block():
        s += "Block " + str(i) + " has invalid hash value!\n"
      if self.chain[i].hash != self.chain[i+1].previous_hash:
        s += "Block " + str(i + 1) + " has invalid previous hash value!\n"
    if not self.chain[len(self.chain) - 1].validate_block():
        s += "Block " + str(len(self.chain) - 1) + " has invalid hash value!\n"
    if s == "":
      s = "Blockchain has been validated! No error found!\n"
    return s
  
  # find certificate using `cert_id` and validate certificate 
  def find_and_validate_cert(self, cert_id):
    found = False
    for x in self.chain[1:]:
      c = Certificate.get_cert_from_string(x.data)
      if c.cert_id.strip() == cert_id.strip():
        found = True
        print("Certificate founded!")
        print("Verifying certificate digital signature...")
        if c.verify_cert():
          print("Verify completed! Certificate is valid!")
          print(c.print_cert())
        else: 
          print("Verify completed! Certificate is invalid!")
    if not found:
      print("Can't find any certificate that match the certificate id provided!") 