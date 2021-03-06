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
from stellar_sdk import Keypair,Server,Network,TransactionBuilder,Asset,ClaimPredicate,Claimant


keypair=Keypair.from_secret("YOURSECRET")
XLM=Asset.native()

predicate=ClaimPredicate.predicate_not(ClaimPredicate.predicate_before_absolute_time(1620584737)) #after quest 5
claimant= Claimant(keypair.public_key,predicate) #you need to create a claimant object

server = Server(horizon_url="https://horizon-testnet.stellar.org")

tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_create_claimable_balance_op(asset=XLM,amount="100",claimants=[claimant])
		.build()
)
tx.sign(keypair.secret)
response = server.submit_transaction(tx)

print("\nTransaction hash: {}".format(response["hash"]))
print("Premi un tasto per continuare")
input()
