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
from math import ceil
from stellar_sdk import Keypair, TransactionBuilder, Network, Server, TransactionEnvelope


#random keypair for example purpose
keypair = Keypair.random()
public = keypair.public_key
secret = keypair.secret
print("Public Key: " + public)
print("Secret Seed: " + secret)
#creation of the account
url = 'https://friendbot.stellar.org'
response = requests.get(url, params={'addr': public})
#network=testnet server=horizon testnet
server = Server(horizon_url="https://horizon-testnet.stellar.org")
network = Network.TESTNET_NETWORK_PASSPHRASE
#anchor authentication url
authurl = 'https://testanchor.stellar.org/auth'
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
b64str = tokenj["token"]
print()
print(b64str)
#every manage data has 2 64chars entry
numdivide = ceil((len(b64str)) / 128)  
#foreach manage data op we add 2 indexing chars
numop = numdivide + ceil( numdivide * 2 / 128)  
#JUST TO SHOW OFF THE ACTUAL SPLIT
print("\nMANAGE DATA OPERATIONS:\n")
for i in range(numop):
	if(i>=0 and i<=9): print("0"+str(i)+b64str[i*62+i*64:(i+1)*62+i*64])
	else: print(str(i)+b64str[i*62+i*64:(i+1)*62+i*64])
	print(b64str[(i+1)*62+i*64:(i+1)*62+(i+1)*64])
	print()
tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=10000) 	
)

for i in range(numop):
	if(i>=0 and i<=9): tx.append_manage_data_op("0"+str(i)+b64str[i*62+i*64:(i+1)*62+i*64],b64str[(i+1)*62+i*64:(i+1)*62+(i+1)*64])
	else: tx.append_manage_data_op(str(i)+b64str[i*62+i*64:(i+1)*62+i*64],b64str[(i+1)*62+i*64:(i+1)*62+(i+1)*64])
	
txtosign=tx.build()
txtosign.sign(keypair)
response = server.submit_transaction(txtosign)
print("\nTransaction hash: {}".format(response["hash"]))
print("Premi un tasto per continuare")
input()
