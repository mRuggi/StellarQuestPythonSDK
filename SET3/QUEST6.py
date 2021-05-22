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

from stellar_sdk import Keypair,Server,Network,TransactionBuilder
import base64
import requests

data=open("name_of_image.png","rb").read() #open the file (binary read)
b64=base64.b64encode(data) #encode it into base 64 string binary

b64str=str(b64)[2:] #convert into a normal string removing b'
print(b64str) #print it
numop=int((len(b64str)+299)/128) #number of op needed to mint the NFT IT NEEDS TO BE <100 for this particular indexing metod 
#lenght of the string+299/128 (every manage data has name and value of 64 bit max)

keypair=Keypair.from_secret("YOURSECRETSHHHH")
print(keypair.public_key)
print()
server = Server(horizon_url="https://horizon-testnet.stellar.org")

#JUST TO SHOW OFF THE ACTUAL SPLIT (you can comment this)
for i in range(numop):
	if(i>=0 and i<=9): print("0"+str(i)+b64str[i*62+i*64:(i+1)*62+i*64])
	else: print(str(i)+b64str[i*62+i*64:(i+1)*62+i*64])
	print(b64str[(i+1)*62+i*64:(i+1)*62+(i+1)*64])
	print()
	
#Building the transaction	
tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=10000) #high fee to avoid network congestion	
)

for i in range(numop):
	if(i>=0 and i<=9): tx.append_manage_data_op("0"+str(i)+b64str[i*62+i*64:(i+1)*62+i*64] , b64str[(i+1)*62+i*64:(i+1)*62+(i+1)*64])
	else: tx.append_manage_data_op(str(i)+b64str[i*62+i*64:(i+1)*62+i*64] , b64str[(i+1)*62+i*64:(i+1)*62+(i+1)*64])
	
txtosign=tx.build()
txtosign.sign(keypair)
response = server.submit_transaction(txtosign)
print("\nTransaction hash: {}".format(response["hash"]))

print("Premi un tasto per continuare")
input()
