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
import requests

keypair=Keypair.from_secret("YOURSECRET")

feepayer=Keypair.random() #create an account that will pay the fee for you 

url = 'https://friendbot.stellar.org'
response = requests.get(url, params={'addr': feepayer.public_key})

destination=Keypair.random() #create the destination for the payment

url = 'https://friendbot.stellar.org'
response = requests.get(url, params={'addr': destination.public_key})

server=Server(horizon_url="https://horizon-testnet.stellar.org")

tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=feepayer.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_payment_op(destination.public_key,"1","XLM",source=keypair.public_key) 
		.build()
)
tx.sign(feepayer.secret) #you need to sign with the feepayer that is the source of the transaction
tx.sign(keypair.secret) #and with your secret because you're doing the payment

response = server.submit_transaction(tx)
print("\nTransaction hash: {}".format(response["hash"]))

print("\nPremi un tasto per continuare")
input()
