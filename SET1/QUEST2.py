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

keypair=Keypair.from_secret("YOURSECRET")
print(keypair.public_key)
receiver="GCXF7WFTCG5TGJLV7H2E5EH2SPF76HFUM3OGDAXDUUACIN4JC6Q6KC34" #anytestnetaccount
server = Server(horizon_url="https://horizon-testnet.stellar.org")

tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_payment_op(receiver,"10","XLM") 
		.build()
)
tx.sign(keypair.secret)
response = server.submit_transaction(tx)
print("\nTransaction hash: {}".format(response["hash"]))
print("Premi un tasto per continuare")
input()
