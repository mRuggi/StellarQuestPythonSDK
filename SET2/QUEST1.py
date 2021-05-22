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

from stellar_sdk import Server,Keypair,TransactionBuilder, Network
import requests

keypair= Keypair.random()  #fund a random account that'll create yours
public= keypair.public_key
secret= keypair.secret
print("Public Key: " + public)
print("Secret Seed: " + secret)

url = 'https://friendbot.stellar.org'
response = requests.get(url, params={'addr': public})

server = Server(horizon_url="https://horizon-testnet.stellar.org")
destinationacc= "YOURSECRET"

transaction= (
	TransactionBuilder(
		source_account = server.load_account(account_id=public), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.add_hash_memo("e3366fcb087bdb2381b7069a19405b748da831c18145eba25654d1092e93ef37")   #add the memo to the transaction
		.append_create_account_op(destination=destinationacc, starting_balance="5000")  #create the account
		.build()
)
transaction.sign(secret)
    
response = server.submit_transaction(transaction)
print("\nTransaction hash: {}".format(response["hash"]))
print("Premi un tasto per continuare")
input()
