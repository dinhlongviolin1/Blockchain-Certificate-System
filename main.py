# import necesasry class
from Blockchain import Blockchain
from Authority import AuthorityList
from Certificate import Certificate

# set new_blockchain to True to reset blockchain (will lose all previous blockchain data)
new_blockchain = False
# set new_authority to True to reset authority (will lose all previous authority)
new_authority = False

# Get all authority from auth instance
def print_all_authority(auth):
  print("Getting all authority:")
  print(auth)

# Get all block from blockchain instance
def print_all_block(bc):
  print("Getting all block in blockchain:")
  print(bc)

# Validate blockchain (check the validity of the hash of each block + check to see whether the current hash match with the previous hash of the next block)
def validate_blockchain(bc):
  print("Validating blockchain...")
  print(bc.validate_blockchain())

# Add new authority 
def add_new_authority(auth):
  print("Add new authority menu\n")
  name = input("Enter authority name: ")
  print("Adding new authority...\n")
  auth.add_new_authority(name)

# Add new certificate to blockchain
def add_new_cert(auth, bc):
  print("Add new certificate menu\n")
  # get public key
  pub_key = input("Enter public key: ").strip()
  auth_name = auth.find_auth(pub_key)
  # check if public key match with any authority
  if(auth_name == ""):
    return print("No authority found! Returning to home menu!")
  else:
    print("Authority found: " + auth_name)
  # enter private key to sign data later on
  priv_key = input("Enter private key: ").strip()
  # check if private key and public key match
  if(Certificate.verify_signature(pub_key, priv_key)):
    print("Public/Private keypair has been verified!")
  else:
    return print("Private key and Public key does not match! Returning to home menu!")
  # get remaining necessary data for certificate
  id_number = input("Enter recipient's national id number: ")
  name = input("Enter recipient's name: ")
  dob = input("Enter recipient's dob (DD/MM/YYYY): ")
  cert_name = input("Enter certficate name: ")
  cert_des = input("Enter certificate description: ")
  issue_date = input("Enter certificate issued date (DD/MM/YYYY): ")
  # create certificate
  a = Certificate(id_number, name, dob, cert_name, cert_des, issue_date, auth_name, pub_key, priv_key)
  print("Certificate has been created successfully")
  print(a.print_cert())
  to_blockchain = input("Do you want to submit this certificate to blockchain? (1 for yes, other for no): ")
  if to_blockchain == "1":
    # add certificate to blockchain
    bc.add_block(str(a))
    print("Please save the Certificate Id (cert_id) to validate this certificate in the blockchain in the future.")
  else:
    print("Exiting to home menu...")

# Find certificate from blockchain and verify with certificate signature
def find_and_verify_cert(bc):
  print("Find and verify certificate menu\n")
  cert_id = input("Enter the certificate id: ")
  bc.find_and_validate_cert(cert_id)

if __name__ == "__main__":
  # Load all data
  print("Loading authority data...")
  auth = AuthorityList(new_authority, "authority.txt")
  print("Loading blockchain data...")
  bc = Blockchain(new_blockchain, "blockchain.txt")
  validate_blockchain(bc)
  print("All data is loaded successfully!")
  loop = True
  # main program loop
  while loop:
    # Select Menu
    print("------------------------------------")
    print("Blockchian Academic Certificate System")
    print("You are currently at home screen...")
    print("Enter 1 to view all authority")
    print("Enter 2 to view all block in the blockchain")
    print("Enter 3 to create new authority")
    print("Enter 4 to create new certificate")
    print("Enter 5 to find and validate certificate")
    print("Enter 0 or other to exit program")
    a = input("Please enter a number to proceed: ")
    print("------------------------------------")
    if a == "1":
      print_all_authority(auth)
    elif a == "2":
      print_all_block(bc)
    elif a == "3":
      add_new_authority(auth)
    elif a == "4":
      add_new_cert(auth, bc)
    elif a == "5":
      find_and_verify_cert(bc)
    else:
      # Exit program if no input match
      print("Exiting program...")
      loop = False