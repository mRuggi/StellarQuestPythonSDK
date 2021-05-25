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
from stellar_sdk import Keypair,Server,Network,TransactionBuilder,Asset
import requests

keypair=Keypair.from_secret("SCVYRQH2IDU5SXPOBUEH6CAOSOWXFXC23DVIHG2O7HJEXF3WINVZLE3E")
print(keypair.public_key)

destination=Keypair.random()
print("Public Key: " + destination.public_key)
print("Secret Seed: " + destination.secret)

url = 'https://friendbot.stellar.org'
response = requests.get(url, params={'addr': destination.public_key})

Asset=Asset("MariusLenk",keypair.public_key)


server = Server(horizon_url="https://horizon-testnet.stellar.org")

tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_change_trust_op(asset_code=Asset.code,asset_issuer=Asset.issuer,source=destination.public_key)
		.append_payment_op(destination.public_key,"10",Asset.code,Asset.issuer)
		.append_clawback_op(asset=Asset,from_=destination.public_key,amount="9",source=keypair.public_key)
		.build()
)
tx.sign(keypair.secret)
tx.sign(destination.secret)

response = server.submit_transaction(tx)
print("\nTransaction hash: {}".format(response["hash"]))
print("Premi un tasto per continuare")
input()
