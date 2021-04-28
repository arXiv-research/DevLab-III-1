/*******************************************************************************
 * This file is part of the IN3 project.
 * Sources: https://github.com/blockchainsllc/in3
 *
 * Copyright (C) 2018-2021 slock.it GmbH, Blockchains LLC
 *
 *
 * COMMERCIAL LICENSE USAGE
 *
 * Licensees holding a valid commercial license may use this file in accordance
 * with the commercial license agreement provided with the Software or, alternatively,
 * in accordance with the terms contained in a written agreement between you and
 * slock.it GmbH/Blockchains LLC. For licensing terms and conditions or further
 * information please contact slock.it at in3@slock.it.
 *
 * Alternatively, this file may be used under the AGPL license as follows:
 *
 * AGPL LICENSE USAGE
 *
 * This program is free software: you can redistribute it and/or modify it under the
 * terms of the GNU Affero General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
 * PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
 * [Permissions of this strong copyleft license are conditioned on making available
 * complete source code of licensed works and modifications, which include larger
 * works using a licensed work, under the same license. Copyright and license notices
 * must be preserved. Contributors provide an express grant of patent rights.]
 * You should have received a copy of the GNU Affero General Public License along
 * with this program. If not, see <https://www.gnu.org/licenses/>.
 *******************************************************************************/

/**
 * return structure after fetching the current account info.
 */
export declare interface ZKAccountInfo {
    address: string,
    committed: {
        balances: {
            [name: string]: number
        },
        nonce: number,
        pubKeyHash: string
    },
    depositing: {
        balances: {
            [name: string]: number
        }
    },
    id: number,
    verified: {
        balances: {
            [name: string]: number
        },
        nonce: number,
        pubKeyHash: string
    }
}
/**
 * Block state.
 */
export declare interface BlockInfo {
    blockNumber: number,
    committed: boolean,
    verified: boolean
}

/**
 * Transaction state
 */
export declare interface TxInfo {
    block: BlockInfo,
    executed: boolean,
    failReason: string,
    success: boolean
}

/**
 * L1 Operation State
 */
export declare interface ETHOpInfoResp {
    executed: boolean,
    block: BlockInfo
}

/**
 * Defines the type of a transaction.
 */
export declare interface TxType {
    type: "Withdraw" | "Transfer" | "TransferToNew"
}

/**
 * fee collection.
 */
export declare interface Fee {
    feeType: TxType,
    totalGas: number,
    gasPrice: number,
    gasFee: number,
    zkpFee: number,
    totalFee: number
}

/**
 * Token List.
 */
export declare interface Tokens {
    [key: string]: Token
}
/** Token representation */
export declare interface Token {
    address: String,
    decimals: number,
    id: number,
    symbol: String
}

/**
 * Response of a Deposit-Transaction.
 */
export declare interface DepositResponse {
    receipt: TransactionReceipt
}

/**
 * API for zksync.
 */
export declare interface ZksyncAPI<BufferType> {

    /**
     * gets current account Infoa and balances.
     * @param account the address of the account . if not specified, the first signer is used.
     */
    getAccountInfo(account?: string): Promise<ZKAccountInfo>

    /**
     * gets the contract address of the zksync contract
     */
    getContractAddress(): Promise<String>

    /**
     * returns the address of the account used.
     */
    getAccountAddress(): String

    /**
     * returns an object containing Token objects with its short name as key
     */
    getTokens(): Promise<Tokens>

    /**
     * get transaction info
     * @param txHash the has of the tx you want the info about
     */
    getTxInfo(txHash: string): Promise<TxInfo>

    /**
     * set the signer key based on the current pk
     * @param tokenSymbol the address of the token
     * @param newKey the seed of the new key ( this is optional, if ommited the derrived key will be set in the rollup)
     */
    setKey(tokenSymbol?: string, newKey?: BufferType | string): Promise<String>

    /**
     * returns the state of receipt of the PriorityOperation
     * @param opId the id of the PriorityOperation
     */
    getEthopInfo(opId: number): Promise<ETHOpInfoResp>

    /**
     * returns the current token price
     * @param tokenSymbol the address of the token
     */
    getTokenPrice(tokenSymbol: string): Promise<Number>

    /**
     * returns the transaction fee
     * @param txType either Withdraw or Transfer
     * @param receipient the address the transaction is send to
     * @param token the token identifier e.g. ETH
     */
    getTxFee(txType: TxType, receipient: string, token: string): Promise<Fee>

    /**
     * returns private key used for signing zksync transactions
     */
    getSyncKey(): String

    /**
     * returns public key used for signing zksync transactions
     */
    getSyncPubKeyHash(): String

    /**
     * returns public key used for signing zksync transactions
     */
    getSyncPubKey(): String

    /**
     * deposits the declared amount into the rollup
     * @param amount amount in wei to deposit
     * @param token the token identifier e.g. ETH
     * @param approveDepositAmountForERC20 bool that is set to true if it is a erc20 token that needs approval
     * @param account address of the account that wants to deposit (if left empty it will be taken from current signer)
     */
    deposit(amount: number, token: string, approveDepositAmountForERC20: boolean, account?: string): Promise<DepositResponse> //in3 error types?

    /**
     * transfers the specified amount to another address within the zksync rollup
     * @param to address of the receipient
     * @param amount amount to send in wei
     * @param token the token indentifier e.g. ETH
     * @param account address of the account that wants to transfer (if left empty it will be taken from current signer)
     */
    transfer(to: string, amount: number, token: string, account?: string): Promise<String> //in3 error types?

    /**
     * withdraws the specified amount from the rollup to a specific address
     * @param ethAddress the receipient address
     * @param amount amount to withdraw in wei
     * @param token the token identifier e.g. ETH
     * @param account address of the account that wants to withdraw (if left empty it will be taken from current signer)
     */
    withdraw(ethAddress: string, amount: number, token: string, account?: string): Promise<String> //in3 error type?

    /**
     * executes an emergency withdrawel onchain
     * @param token the token identifier e.g. ETH
     */
    emergencyWithdraw(token: string): Promise<String> //in3 error type?

    /**
     * signs the message based on the config and returns a Musig Schnorr signature
     * @param msg the message
     */
    sign(msg: string): Promise<String> //in3 error type?

    /**
     * verifies a Musig Schnorr signature
     * @param msg the message
     * @param sig the 96byte long signature
     */
    verify(msg: string, sig: string): boolean

    /**
     * aggregates the given publickeys into one public key for a Musig Schnorr signature
     * @param pubkeys the packed public keys (either a concatenated string or as array of public keys)
     */
    aggregatePubKey(pubkeys: string | string[]): string
}


/**
 * zksync configuration.
 */
export declare interface zksync_config {
    /**
     * url of the zksync-server
     */
    provider_url?: string

    /**
    * the account to be used. if not specified, the first signer will be used.
    */
    account?: string

    /**
     * defines the type of the signer. Must be one of those 3 values. (default: pk)
     */
    signer_type?: 'pk' | 'contract' | 'create2'

    /**
     * optionaly the private seephrase to use when signing sync-transaction.
     * If ommited this key is derrived from the signer.
     */
    sync_key?: string

    /**
     * create2 arguments
     */
    create2?: {
        /**
         * the address of creator of the contract
         */
        creator: string

        /**
         * the codehash of the deploy-tx (including constructor arguments)
         */
        codehash: string

        /**
         * the saltarg, which is added to the pub_key_has of the sync_key
         */
        saltarg: string
    }

    /** 
     * if used as a musig-signature the 
     */
    musig_urls?: string[]

    /** 
     * concated packed public keys of the signers of the multisig
     */
    musig_pub_keys?: string



}


/*
public zksync:ZksyncAPI<BufferType>
 */
