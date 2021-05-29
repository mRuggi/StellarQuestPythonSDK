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
from stellar_sdk import Keypair,Server,Network,TransactionBuilder,TransactionEnvelope,Account

keypair = Keypair.from_secret("YOURSECRET")
print(keypair.public_key)

server = Server(horizon_url="https://horizon-testnet.stellar.org")
acc=server.load_account(keypair.public_key) #fetch current sequence number
acc.increment_sequence_number() #increment the sequence number

preauthtx= (
	TransactionBuilder(
		source_account = acc, #use the incremented sequence number to create a "future" transaction
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_manage_data_op("This is from the future","<3")		
)
x=preauthtx.build() #when using the build() method the sequence number of acc is incremented
authhash=x.hash() #need the hash of the pre-authorized transaction 

tx=(
	TransactionBuilder(
		source_account = server.load_account(keypair.public_key), #must fetch current sequence number again
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_pre_auth_tx_signer(authhash,1) #set the pre auth transaction as a signer
		.build() #build as usual
)
tx.sign(keypair) #sign
response = server.submit_transaction(tx) 
print("\nTransaction hash: {}".format(response["hash"]))

#And here's the magic:
response = server.submit_transaction(x) 
#you can submit the pre authorized transaction without signing
#because you set that as a pre authorized transaction signer
print("\nTransaction hash: {}".format(response["hash"]))


print("Premi un tasto per continuare")
input()
