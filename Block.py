import hashlib as hasher
import datetime as date
# Define Block
class Block:
  def __init__(self, index, timestamp, data, previous_hash):
    self.index = index
    self.timestamp = timestamp
    self.data = data
    self.previous_hash = previous_hash
    self.hash = self.hash_block()
  
  # hash function for the whole block
  def hash_block(self):
    sha = hasher.sha256()
    sha.update(str(self.index).encode('utf-8') + str(self.timestamp).encode('utf-8') + str(self.data).encode('utf-8') + str(self.previous_hash).encode('utf-8'))
    return sha.hexdigest()

  # validate the current hash with the hash of the whole block to see if it match
  def validate_block(self):
    return self.hash == self.hash_block()
  
  def set_hash(self, hash1): 
    self.hash = hash1

  def __str__(self):
    return str(self.index) + " *** " + str(self.timestamp) + " *** " + str(self.data) + " *** " + str(self.previous_hash) + " *** " + str(self.hash)
  
  # Generate genesis block
  @staticmethod
  def create_genesis_block():
  # Manually construct a block with
  # index zero and arbitrary previous hash
    return Block(0, date.datetime.now(), "Genesis Block", "0")
  
  # Generate all later blocks in the blockchain
  @staticmethod
  def create_next_block(last_block, data):
    this_index = last_block.index + 1
    this_timestamp = str(date.datetime.now())
    this_data = data
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)