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

SRT=Asset("SRT","GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B")
XLM=Asset.native()
keypair=Keypair.from_secret("YOURSECRET")

server = Server(horizon_url="https://horizon-testnet.stellar.org")

path=[] #needs to be a one way path

tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_change_trust_op(SRT.code,SRT.issuer)
		.append_path_payment_strict_send_op(SRT.issuer,XLM.code,XLM.issuer,"1",SRT.code,SRT.issuer,"1",path)
		.build()
)
tx.sign(keypair.secret)

response = server.submit_transaction(tx)
print("\nTransaction hash: {}".format(response["hash"]))
print("Premi un tasto per continuare")
input()
