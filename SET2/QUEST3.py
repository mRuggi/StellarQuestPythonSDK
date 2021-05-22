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

feepayer=Keypair.random() #random fee payer account funded by friendbot

url = 'https://friendbot.stellar.org'
response = requests.get(url, params={'addr': feepayer.public_key})

server = Server(horizon_url="https://horizon-testnet.stellar.org")

tx= (         #this will be the transaction envelope we'll use for fee bump
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_payment_op(keypair.public_key,"1","XLM") 
		.build()
)
tx.sign(keypair.secret) #needs to be signed and then wrapped

fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
    fee_source=feepayer,
    base_fee=200,
    inner_transaction_envelope=tx, #set the previous transaction as inner envelope
    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 

)
fee_bump_tx.sign(feepayer.secret)
response = server.submit_transaction(fee_bump_tx)

response = server.submit_transaction(tx)
print("\nTransaction hash: {}".format(response["hash"]))
print("Premi un tasto per continuare")
input()
