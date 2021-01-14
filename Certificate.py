import rsa
import uuid

# define certificate
class Certificate:
  def __init__(self, national_id, name, dob, cert_name, cert_detail, issued_date, authority_name, public_key, private_key, cert_id = "", hasPrivateKey = True):
    if cert_id == "":
      self.cert_id = str(uuid.uuid4())
    else:
      self.cert_id = cert_id
    self.national_id = national_id
    self.name = name
    self.dob = dob
    self.cert_name = cert_name
    self.cert_detail = cert_detail
    self.issued_date = issued_date
    self.authority_name = authority_name
    self.public_key = public_key
    if hasPrivateKey:
      self.signature = self.sign_cert(private_key)
    else:
      self.signature = private_key

  # to string method
  def __str__(self):
    return " $$!! ".join([self.cert_id,self.national_id, self.name, self.dob, self.cert_name, self.cert_detail, self.issued_date, self.authority_name, self.public_key, self.signature])

  # print cert with a format
  def print_cert(self):
    s = "---------------------------------------------------\n"
    s += self.cert_name + "\n"
    s += self.cert_detail + "\n"
    s += "This Certificate Is Awarded To: \nName: " + self.name
    s += "\nDOB: " + self.dob
    s += "\nNational Id Number: " + self.national_id + "\n"
    s += "Issued By: " + self.authority_name + "\n"
    s += "Issued Date: " + self.issued_date + "\n"
    s += "Certificate Id: " + self.cert_id + "\n"
    s += "Digital Signature: " + self.signature + "\n"
    s += "Public Key: " + self.public_key + "\n"
    s += "---------------------------------------------------\n"
    return s

  # sign certificate (hash the whole cert and encrypt with private key)
  def sign_cert(self, priv):
    priv_key = rsa.PrivateKey.load_pkcs1("\n".join(priv.split("!!!")).encode('utf-8'))
    m = str(self.cert_id).encode('utf-8') + str(self.national_id).encode('utf-8') + str(self.name).encode('utf-8') + str(self.dob).encode('utf-8') + str(self.cert_name).encode('utf-8') + str(self.cert_detail).encode('utf-8') + str(self.issued_date).encode('utf-8') +(self.authority_name).encode('utf-8') + str(self.public_key).encode('utf-8')
    signed = rsa.sign(m, priv_key, 'SHA-256')
    return str(signed)

  # verify certificate validity
  def verify_cert(self):
    pub_key = rsa.PublicKey.load_pkcs1("\n".join(self.public_key.split("!!!")).encode('utf-8'))
    m = str(self.cert_id).encode('utf-8') + str(self.national_id).encode('utf-8') + str(self.name).encode('utf-8') + str(self.dob).encode('utf-8') + str(self.cert_name).encode('utf-8') + str(self.cert_detail).encode('utf-8') + str(self.issued_date).encode('utf-8') +(self.authority_name).encode('utf-8') + str(self.public_key).encode('utf-8')
    try:
      hash_method = rsa.verify(m, eval(self.signature), pub_key)
    except:
      return False
    return hash_method == "SHA-256"

  # get Certificate from string (parsing data from blockchain)
  @staticmethod
  def get_cert_from_string(s):
    data = s.strip().split(" $$!! ")
    a = Certificate(data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[0], False)
    return a
  
  # verfiy the public/private keypair when creating certificate
  @staticmethod
  def verify_signature(pub, priv):
    pub_key = rsa.PublicKey.load_pkcs1("\n".join(pub.split("!!!")).encode('utf-8'))
    private_key = rsa.PrivateKey.load_pkcs1("\n".join(priv.split("!!!")).encode('utf-8'))
    message = "test"
    crypto = rsa.encrypt(message.encode('utf-8'), pub_key)
    try:
      decrypt = rsa.decrypt(crypto, private_key)
    except:
      return False
    return decrypt.decode('utf-8') == message
