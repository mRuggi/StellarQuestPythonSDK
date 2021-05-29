#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  
#  
#  Copyright 2021 mRuggi <mRuggi@PC>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import json
import requests
from stellar_sdk import Keypair, TransactionBuilder, Network, Server, TransactionEnvelope, Asset

#random keypair for example purpose
keypair = Keypair.random()
public = keypair.public_key
secret = keypair.secret
print("Public Key: " + public)
print("Secret Seed: " + secret)

#creation of the account
url = 'https://friendbot.stellar.org'
response = requests.get(url, params={'addr': public})

#anchor authentication url
authurl = 'https://testanchor.stellar.org/auth'
network = Network.TESTNET_NETWORK_PASSPHRASE
#GET request for the challenge transaction
challengerequest = requests.get(authurl, params='account=' + str(public))
response = challengerequest.json()
#from the response we need the xdr of the challenge transaction to sign
xdr = response["transaction"]
print()
print(xdr)

#create a Transaction Envelope from the xdr and sign it
a = TransactionEnvelope.from_xdr(xdr, network)
a.sign(secret)

#convert the signed Transaction Envelope to a new xdr to POST
xdr1 = a.to_xdr()
print()
print(xdr1)

#reuse of the response variable to store the new xdr
response["transaction"] = xdr1
#POST request with the signed transaction
tokenreq = requests.post(authurl, response)
#from the response we need the token
tokenj = tokenreq.json()
tokens = tokenj["token"]
print("\nToken:")
print(tokens)

#anchor SEP12 
kycurl = 'https://testanchor.stellar.org/kyc/customer'
authorization={
'Authorization': 'Bearer '+tokens, #string header
}
kycvalues={    #data JSON (python dictionary)
  "account": public,
  "first_name": "Name",
  "last_name": "Surname",
  "email_address": "test@testmail.com",
  "bank_account_number": "123456",
  "bank_number": "12345"
}
response = requests.put(kycurl, headers=authorization, params={'account':public}, data=kycvalues)
response = requests.get(kycurl, headers=authorization, params={'account':public})
print()
print(response.json())

#Trustline to receive MULT

server = Server(horizon_url="https://horizon-testnet.stellar.org")
MULT=Asset("MULT","GDLD3SOLYJTBEAK5IU4LDS44UMBND262IXPJB3LDHXOZ3S2QQRD5FSMM")

tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=public), 
		network_passphrase=network, 
		base_fee=100) 
		.append_change_trust_op(MULT.code,MULT.issuer) 
		.build()
)
tx.sign(keypair)
txresponse = server.submit_transaction(tx)
print("\nTransaction hash: {}".format(txresponse["hash"]))

#anchor SEP6
transferurl = 'https://testanchor.stellar.org/sep6/deposit'
query={
'asset_code':'MULT',
'account':public,
'type':'bank_account',
'amount':100
}
response = requests.get(transferurl, headers=authorization, params=query)
print()
print(response.json())

print("\nPremi un tasto per continuare")
input()
