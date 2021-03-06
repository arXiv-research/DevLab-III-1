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


/** a  Receipt of a Transaction containing the events and execution status */
export type TransactionReceipt = {
    /** 32 Bytes - hash of the block where this transaction was in. */
    blockHash: Hash
    /** block number where this transaction was in.*/
    blockNumber: BlockType
    /** 20 Bytes - The contract address created, if the transaction was a contract creation, otherwise null.*/
    contractAddress: Address
    /** The total amount of gas used when this transaction was executed in the block. */
    cumulativeGasUsed: Quantity
    /** 20 Bytes - The address of the sender. */
    from: Address
    /** 20 Bytes - The address of the receiver. null when it???s a contract creation transaction.*/
    to: Address
    /** The amount of gas used by this specific transaction alone. */
    gasUsed: Quantity
    /** Array of log objects, which this transaction generated. */
    logs: Log[]
    /** 256 Bytes - A bloom filter of logs/events generated by contracts during transaction execution. Used to efficiently rule out transactions without expected logs.*/
    logsBloom: Data
    /** 32 Bytes - Merkle root of the state trie after the transaction has been executed (optional after Byzantium hard fork EIP609)*/
    root?: Hash
    /** 0x0 indicates transaction failure , 0x1 indicates transaction success. Set for blocks mined after Byzantium hard fork EIP609, null before. */
    status: Quantity
    /** 32 Bytes - hash of the transaction. */
    transactionHash: Hash
    /** Integer of the transactions index position in the block. */
    transactionIndex: Quantity
    /** event objects, which are only added in the web3Contract */
    events?: {
        [name: string]: {
            returnValues: any
        }
    }
}
export type TransactionDetail = {
    /**  32 Bytes - hash of the transaction. */
    hash: Hash
    /** the number of transactions made by the sender prior to this one.*/
    nonce: Quantity
    /** 32 Bytes - hash of the block where this transaction was in. null when its pending.*/
    blockHash: Hash
    /** block number where this transaction was in. null when its pending.*/
    blockNumber: BlockType
    /** integer of the transactions index position in the block. null when its pending.*/
    transactionIndex: Quantity
    /** 20 Bytes - address of the sender.*/
    from: Address
    /** 20 Bytes - address of the receiver. null when its a contract creation transaction. */
    to: Address
    /**  value transferred in Wei.*/
    value: Quantity
    /** gas price provided by the sender in Wei.*/
    gasPrice: Quantity
    /** gas provided by the sender. */
    gas: Quantity
    /** the data send along with the transaction. */
    input: Data
    /** the standardised V field of the signature.*/
    v: Quantity
    /** the standardised V field of the signature (0 or 1).*/
    standardV: Quantity
    /** the R field of the signature.*/
    r: Quantity
    /** raw transaction data */
    raw: Data
    /** public key of the signer. */
    publicKey: Hash
    /** the chain id of the transaction, if any. */
    chainId: Quantity
    /** creates contract address */
    creates: Address
    /** (optional) conditional submission, Block number in block or timestamp in time or null. (parity-feature)    */
    condition?: any
    /** optional: the private key to use for signing */
    pk?: any
}

export type Block = {
    /**  The block number. null when its pending block */
    number: Quantity
    /** hash of the block. null when its pending block */
    hash: Hash
    /** hash of the parent block */
    parentHash: Hash
    /** 8 bytes hash of the generated proof-of-work. null when its pending block. Missing in case of PoA. */
    nonce: Data
    /** SHA3 of the uncles data in the block */
    sha3Uncles: Data
    /** 256 Bytes - the bloom filter for the logs of the block. null when its pending block */
    logsBloom: Data
    /** 32 Bytes - the root of the transaction trie of the block */
    transactionsRoot: Data
    /** 32 Bytes - the root of the final state trie of the block */
    stateRoot: Data
    /** 32 Bytes - the root of the receipts trie of the block */
    receiptsRoot: Data
    /** 20 Bytes - the address of the author of the block (the beneficiary to whom the mining rewards were given)*/
    author: Address
    /** 20 Bytes - alias of ???author???*/
    miner: Address
    /** integer of the difficulty for this block */
    difficulty: Quantity
    /** integer of the total difficulty of the chain until this block */
    totalDifficulty: Quantity
    /** the ???extra data??? field of this block */
    extraData: Data
    /** integer the size of this block in bytes */
    size: Quantity
    /** the maximum gas allowed in this block */
    gasLimit: Quantity
    /** the total used gas by all transactions in this block */
    gasUsed: Quantity
    /** the unix timestamp for when the block was collated */
    timestamp: Quantity
    /** Array of transaction objects, or 32 Bytes transaction hashes depending on the last given parameter */
    transactions: (Hash | Transaction)[]
    /** Array of uncle hashes */
    uncles: Hash[]
    /** PoA-Fields */
    sealFields: Data[]
}
export type Log = {
    /** true when the log was removed, due to a chain reorganization. false if its a valid log. */
    removed: boolean
    /** integer of the log index position in the block. null when its pending log. */
    logIndex: Quantity
    /** integer of the transactions index position log was created from. null when its pending log. */
    transactionIndex: Quantity
    /** Hash, 32 Bytes - hash of the transactions this log was created from. null when its pending log. */
    transactionHash: Hash
    /** Hash, 32 Bytes - hash of the block where this log was in. null when its pending. null when its pending log. */
    blockHash: Hash,
    /** the block number where this log was in. null when its pending. null when its pending log. */
    blockNumber: Quantity
    /** 20 Bytes - address from which this log originated. */
    address: Address,
    /**  contains the non-indexed arguments of the log. */
    data: Data
    /** - Array of 0 to 4 32 Bytes DATA of indexed log arguments. (In solidity: The first topic is the hash of the signature of the event (e.g. Deposit(address,bytes32,uint256)), except you declared the event with the anonymous specifier.) */
    topics: Data[]
}

export type LogFilter = {
    /**  Quantity or Tag - (optional) (default: latest) Integer block number, or 'latest' for the last mined block or 'pending', 'earliest' for not yet mined transactions. */
    fromBlock?: BlockType
    /** Quantity or Tag - (optional) (default: latest) Integer block number, or 'latest' for the last mined block or 'pending', 'earliest' for not yet mined transactions.*/
    toBlock?: BlockType
    /** (optional) 20 Bytes - Contract address or a list of addresses from which logs should originate.*/
    address: Address
    /** (optional) Array of 32 Bytes Data topics. Topics are order-dependent. It???s possible to pass in null to match any topic, or a subarray of multiple topics of which one should be matching. */
    topics?: (string | string[])[]
    /** ??(optional) The maximum number of entries to retrieve (latest first). */
    limit?: Quantity
}

export type TxRequest = {
    /** contract */
    to?: Address

    /** address of the account to use */
    from?: Address

    /** the data to send */
    data?: Data

    /** the gas needed */
    gas?: number

    /** the gasPrice used */
    gasPrice?: number

    /** the nonce */
    nonce?: number

    /** the value in wei */
    value?: Quantity

    /** the ABI of the method to be used */
    method?: string

    /** the argument to pass to the method */
    args?: any[]

    /**raw private key in order to sign */
    pk?: Hash

    /**  number of block to wait before confirming*/
    confirmations?: number

    /** number of seconds to wait for confirmations before giving up. Default: 10 */
    timeout?: number
}

export interface Web3Event {
    returnValues: {
        [name: string]: any
    },
    event: string,
    signature: string,
    logIndex: number
    transactionIndex: number,
    transactionHash: Hash,
    address: Address
    blockNumber: number
    blockHash: Hash,
    raw: {
        data: Hex
        topicx: Hash[]
    }


}

/**
 * The Account API
 */
export interface AccountAPI<BufferType> {

    /**
     * adds a private key to sign with.
     * This method returns address of the pk
     * @param pk
     */
    add(pk: string | BufferType): Promise<string>


}

export interface Web3TransactionObject {
    call: (options?: {
        gasPrice?: string | number | bigint,
        gas?: string | number | bigint,
        to?: Address,
        from?: Address,
    }) => Promise<any>,
    send: (options?: {
        gasPrice?: string | number | bigint,
        gas?: string | number | bigint,
        nonce?: string | number | bigint,
        to?: Address,
        from?: Address,
        value?: number | string | bigint
    }) => Promise<any>,
    estimateGas: (options?: {
        value?: string | number | bigint,
        gas?: string | number | bigint,
        to?: Address,
        from?: Address,
    }) => Promise<number>,
    encodeABI: () => Hex
}

export interface Web3Contract {
    options: {
        address: Address,
        jsonInterface: ABI[],
        gasPrice?: string | number | bigint,
        gas?: string | number | bigint,
        from?: Address,
        data?: Hex,
        transactionConfirmationBlocks: number,
        transactionPollingTimeout: number
    },
    deploy?: (args: {
        data: string,
        arguments?: any[]
    }) => Web3TransactionObject,
    methods: {
        [methodName: string]: (...args: any) => Web3TransactionObject
    },

    once: (eventName: string, options: {}, handler: (error?: Error, evData?: Web3Event) => void) => void,

    events: {
        [eventName: string]: (options?: {
            fromBlock?: number,
            toBlock?: number,
            topics?: any[],
            filter?: { [indexedName: string]: any }
        }) => {
            on: (ev: 'data' | 'error', handler: (ev: Web3Event | Error) => void) => any
            once: (ev: 'data', handler: (ev: Web3Event) => void) => any
            off: (ev: string, handler: (ev: any) => void) => any
        }
    },

    getPastEvents(evName: string, options?: {
        fromBlock?: number,
        toBlock?: number,
        topics?: any[],
        filter?: { [indexedName: string]: any }
    }): Promise<Web3Event[]>

}

/**
 * The API for ethereum operations.
 */
export interface EthAPI<BigIntType, BufferType> {
    /**
     * the client used.
     */
    client: IN3Generic<BigIntType, BufferType>;

    /**
     * a custom signer
     */
    signer?: Signer<BigIntType, BufferType>;

    /**
     * accounts-API
     */
    accounts: AccountAPI<BufferType>;

    constructor(client: IN3Generic<BigIntType, BufferType>): EthAPI<BigIntType, BufferType>;
    /**
     * Returns the number of most recent block. (as number)
     */
    blockNumber(): Promise<number>;
    /**
     * Returns the current price per gas in wei. (as number)
     */
    gasPrice(): Promise<number>;
    /**
     * Executes a new message call immediately without creating a transaction on the block chain.
     */
    call(tx: Transaction, block?: BlockType): Promise<string>;
    /**
     * Executes a function of a contract, by passing a [method-signature](https://github.com/ethereumjs/ethereumjs-abi/blob/master/README.md#simple-encoding-and-decoding) and the arguments, which will then be ABI-encoded and send as eth_call.
     */
    callFn(to: Address, method: string, ...args: any[]): Promise<any>;
    /**
     * Returns the EIP155 chain ID used for transaction signing at the current best block. Null is returned if not available.
     */
    chainId(): Promise<string>;
    /**
     * Returns the clientVersion. This may differ in case of an network, depending on the node it communicates with.
     */
    clientVersion(): Promise<string>;
    /**
     * Makes a call or transaction, which won???t be added to the blockchain and returns the used gas, which can be used for estimating the used gas.
     */
    estimateGas(tx: Transaction): Promise<number>;
    /**
     * Returns the balance of the account of given address in wei (as hex).
     */
    getBalance(address: Address, block?: BlockType): Promise<BigIntType>;
    /**
     * Returns code at a given address.
     */
    getCode(address: Address, block?: BlockType): Promise<string>;
    /**
     * Returns the value from a storage position at a given address.
     */
    getStorageAt(address: Address, pos: Quantity, block?: BlockType): Promise<string>;
    /**
     * Returns information about a block by hash.
     */
    getBlockByHash(hash: Hash, includeTransactions?: boolean): Promise<Block>;
    /**
     * Returns information about a block by block number.
     */
    getBlockByNumber(block?: BlockType, includeTransactions?: boolean): Promise<Block>;
    /**
     * Returns the number of transactions in a block from a block matching the given block hash.
     */
    getBlockTransactionCountByHash(block: Hash): Promise<number>;
    /**
     * Returns the number of transactions in a block from a block matching the given block number.
     */
    getBlockTransactionCountByNumber(block: Hash): Promise<number>;
    /**
     * Polling method for a filter, which returns an array of logs which occurred since last poll.
     */
    getFilterChanges(id: Quantity): Promise<Log[]>;
    /**
     * Returns an array of all logs matching filter with given id.
     */
    getFilterLogs(id: Quantity): Promise<Log[]>;
    /**
     * Returns an array of all logs matching a given filter object.
     */
    getLogs(filter: LogFilter): Promise<Log[]>;
    /**
     * Returns information about a transaction by block hash and transaction index position.
     */
    getTransactionByBlockHashAndIndex(hash: Hash, pos: Quantity): Promise<TransactionDetail>;
    /**
     * Returns information about a transaction by block number and transaction index position.
     */
    getTransactionByBlockNumberAndIndex(block: BlockType, pos: Quantity): Promise<TransactionDetail>;
    /**
     * Returns the information about a transaction requested by transaction hash.
     */
    getTransactionByHash(hash: Hash): Promise<TransactionDetail>;
    /**
     * Returns the number of transactions sent from an address. (as number)
     */
    getTransactionCount(address: Address, block?: BlockType): Promise<number>;

    /**
     * returns the public addresses  accounts
     */
    getAccounts(): Promise<Address[]>

    /**
     * Returns the receipt of a transaction by transaction hash.
     * Note That the receipt is available even for pending transactions.
     */
    getTransactionReceipt(hash: Hash): Promise<TransactionReceipt>;
    /**
     * Returns information about a uncle of a block by hash and uncle index position.
     * Note: An uncle doesn???t contain individual transactions.
     */
    getUncleByBlockHashAndIndex(hash: Hash, pos: Quantity): Promise<Block>;
    /**
     * Returns information about a uncle of a block number and uncle index position.
     * Note: An uncle doesn???t contain individual transactions.
     */
    getUncleByBlockNumberAndIndex(block: BlockType, pos: Quantity): Promise<Block>;
    /**
     * Returns the number of uncles in a block from a block matching the given block hash.
     */
    getUncleCountByBlockHash(hash: Hash): Promise<number>;
    /**
     * Returns the number of uncles in a block from a block matching the given block hash.
     */
    getUncleCountByBlockNumber(block: BlockType): Promise<number>;
    /**
     * Creates a filter in the node, to notify when a new block arrives. To check if the state has changed, call eth_getFilterChanges.
     */
    newBlockFilter(): Promise<string>;
    /**
     * Creates a filter object, based on filter options, to notify when the state changes (logs). To check if the state has changed, call eth_getFilterChanges.
     *
     * A note on specifying topic filters:
     * Topics are order-dependent. A transaction with a log with topics [A, B] will be matched by the following topic filters:
     *
     * [] ???anything???
     * [A] ???A in first position (and anything after)???
     * [null, B] ???anything in first position AND B in second position (and anything after)???
     * [A, B] ???A in first position AND B in second position (and anything after)???
     * [[A, B], [A, B]] ???(A OR B) in first position AND (A OR B) in second position (and anything after)???
     */
    newFilter(filter: LogFilter): Promise<string>;
    /**
     * Creates a filter in the node, to notify when new pending transactions arrive.
     *
     * To check if the state has changed, call eth_getFilterChanges.
     */
    newPendingTransactionFilter(): Promise<string>;
    /**
     * Uninstalls a filter with given id. Should always be called when watch is no longer needed. Additonally Filters timeout when they aren???t requested with eth_getFilterChanges for a period of time.
     */
    uninstallFilter(id: Quantity): Promise<Quantity>;
    /**
     * Returns the current ethereum protocol version.
     */
    protocolVersion(): Promise<string>;
    /**
     * Returns the value in wei as hexstring.
     */
    toWei(value: string, unit: string): string;
    /**
      * Returns the state of the underlying node.
      */
    syncing(): Promise<boolean | {
        startingBlock: Hex;
        currentBlock: Hex;
        highestBlock: Hex;
        blockGap: Hex[][];
        warpChunksAmount: Hex;
        warpChunksProcessed: Hex;
    }>;

    /**
     * resolves a name as an ENS-Domain.
     * @param name the domain name
     * @param type the type (currently only addr is supported)
     * @param registry optionally the address of the registry (default is the mainnet ens registry)
     */
    resolveENS(name: string, type: Address, registry?: string): Promise<Address>;

    /**
     * Creates new message call transaction or a contract creation for signed transactions.
     */
    sendRawTransaction(data: Data): Promise<string>;
    /**
     * signs any kind of message using the `\x19Ethereum Signed Message:\n`-prefix
     * @param account the address to sign the message with (if this is a 32-bytes hex-string it will be used as private key)
     * @param data the data to sign (Buffer, hexstring or utf8-string)
     */
    sign(account: Address, data: Data): Promise<BufferType>;
    /** sends a Transaction */
    sendTransaction(args: TxRequest): Promise<string | TransactionReceipt>;

    web3ContractAt(abi: ABI[], address?: Address, options?: {
        gasPrice?: string | number | bigint,
        gas?: string | number | bigint,
        from?: Address,
        data?: Hex
    }): Web3Contract

    contractAt(abi: ABI[], address?: Address): {
        [methodName: string]: any;
        _address: Address;
        _eventHashes: any;
        events: {
            [event: string]: {
                getLogs: (options: {
                    limit?: number;
                    fromBlock?: BlockType;
                    toBlock?: BlockType;
                    topics?: any[];
                    filter?: {
                        [key: string]: any;
                    };
                }) => Promise<{
                    [key: string]: any;
                    event: string;
                    log: Log;
                }[]>;
            };
            all: {
                getLogs: (options: {
                    limit?: number;
                    fromBlock?: BlockType;
                    toBlock?: BlockType;
                    topics?: any[];
                    filter?: {
                        [key: string]: any;
                    };
                }) => Promise<{
                    [key: string]: any;
                    event: string;
                    log: Log;
                }[]>;
            };
            decode: any;
        };
        _abi: ABI[];
        _in3: IN3Generic<BigIntType, BufferType>;
    };
    decodeEventData(log: Log, d: ABI): any;
    hashMessage(data: Data): Hex;


}
