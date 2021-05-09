#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  AddSigner.py
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

keypair=Keypair.from_secret("SAEPT3H2H3RNJIRLVYC5USEGTHHY4IXAYWNSVSIU2WHHR3JE2BYCQXOG")
issuer=Keypair.from_secret("SCPBX4R6WCBD3KRR4YFVTHZ5V5ZUEJR2YZQIGZUHGHOK5ZPARDH3W43F")
public=issuer.public_key
MXLM=Asset("MXLM",public)


server = Server(horizon_url="https://horizon-testnet.stellar.org")

tx= (
	TransactionBuilder(
		source_account = server.load_account(account_id=keypair.public_key), 
		network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE, 
		base_fee=100) 
		.append_change_trust_op(MXLM.code,MXLM.issuer) 
		.append_payment_op(keypair.public_key,"100",MXLM.code,MXLM.issuer,public) 
		.build()
)
tx.sign(keypair.secret)
tx.sign(issuer.secret)

response = server.submit_transaction(tx)
print("\nTransaction hash: {}".format(response["hash"]))

print("Premi un tasto per continuare")
input()
