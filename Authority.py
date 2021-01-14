import rsa
import os.path

# List of authority
class AuthorityList:
  def __init__(self, isNew, filename):
    self.list = []
    self.file = filename
    if isNew:
      # reset data, delete all authority
      f = open(self.file, "w")
      f.write("")
      f.close()
      print("Authority data reset successfully!")
    else:
      # get authority from text file
      self.get_authority_from_file()
      print("Authority data loaded successfully (" + str(len(self.list)) + " authorities)!")

  # open text file and get authority
  def get_authority_from_file(self):
    if os.path.isfile(self.file):
      f = open(self.file, "r")
      for x in f:
        data = x.strip().split(" *** ")
        self.list.append(Authority(data[0], "\n".join(data[1].split("!!!"))))
      f.close()

  # Create new authority and add to file
  def add_new_authority(self, name):
    new_authority = Authority.create_authority(name)
    f = open(self.file, "a")
    f.write(str(new_authority)+ "\n")
    f.close()
    self.list.append(new_authority)
  
  # str() format for AuthorityList (useful for printing to console and file)
  def __str__(self):
    s = ""
    i = 1
    for x in self.list:
      s += "\nAuthority " + str(i) + ":\n"
      s += "--> Name: " + x.name + "\n"
      s += "--> Public key: " + "\n" + str("!!!".join((x.public_key).split("\n"))) + "\n"
      i = i + 1
    return s
  
  # find authority using public key
  def find_auth(self, key):
    key_format = "\n".join(key.split("!!!"))
    for x in self.list:
      if x.public_key == key_format:
        return x.name
    return ""

class Authority: 
  def __init__(self, name, public_key):
    self.name = name
    self.public_key = public_key
  
  # to string method (useful for printing)
  def __str__(self):
    return str(self.name) + " *** " + str("!!!".join((self.public_key).split("\n")))

  # Static method to create authority
  @staticmethod
  def create_authority(name):
    (pubkey, privkey) = rsa.newkeys(512)
    print("Successfully Generated Authority: " + str(name) + "\n")
    print("Authority Public Key (Id): \n")
    print("!!!".join(pubkey.save_pkcs1().decode("utf-8").split("\n")))
    print("\nAuthority Private Key: \n")
    print("!!!".join(privkey.save_pkcs1().decode("utf-8").split("\n")))
    print("\nPlease save the Public and Private Key so you can submit certificate later! The Private Key is generated only once and cannot be retrieved!\n")
    return Authority(name, pubkey.save_pkcs1().decode("utf-8"))