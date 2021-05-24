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
from stellar_sdk import Keypair,Server,Network,TransactionBuilder,Signer

keypair=Keypair.from_secret("YOURSECRET")
signer=Signer.ed25519_public_key("GBIEZGSGT5LL2FCVNW5DC7WOD5UNMR32XPBB7F43WAK22CKELBUVMXT7",1) #anytestnetaccount you have the secret
print(keypair.public_key)
print(keypair.secret)

server = Server(horizon_url="https://horizon-testnet.stellar.org")

tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_set_options_op(signer=signer) 
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
		.append_payment_op("GBIEZGSGT5LL2FCVNW5DC7WOD5UNMR32XPBB7F43WAK22CKELBUVMXT7","10","XLM")  #you can do any operation here
		.build()
)
tx1.sign("SC6WEJRB6FFHYPEKDGERCJFRKHXNOZKKKNP42EU6LN5RI3VSFCPCS5JK") #sign with the secret of the signer you just added
response = server.submit_transaction(tx1)
print("\nTransaction hash: {}".format(response["hash"]))

print("Premi un tasto per continuare")
input()
