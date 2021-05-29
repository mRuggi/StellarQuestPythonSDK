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

#python has a lot of methods and libraries to get the sha256 of hashx
#also in this quest you need to find the correct hashx :)
keypair = Keypair.from_secret("YOURSECRET")
print(keypair.public_key)
hashx = b'mruggi' #binary string
sha256="05917dddc0143703e4407477b9dea70c0b646734789ff812d2d0b4382b7d3485" #sha256 of hashx

server = Server(horizon_url="https://horizon-testnet.stellar.org")

tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_hashx_signer(sha256,1)	
		.build()
)
tx.sign(keypair.secret)
response = server.submit_transaction(tx)
print("\nTransaction hash: {}".format(response["hash"]))

tx1= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_hashx_signer(sha256,0)	
		.build()
)
tx1.sign_hashx(hashx)
response = server.submit_transaction(tx1)
print("\nTransaction hash: {}".format(response["hash"]))

print("Premi un tasto per continuare")
input()
