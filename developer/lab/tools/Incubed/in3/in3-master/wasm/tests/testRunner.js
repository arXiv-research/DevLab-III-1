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

const fs = require('fs')
const target_platform = process.env.IN3_TARGET || 'index'
const IN3 = require('./in3/' + target_platform + '.js')
const { util } = require('in3-common')
const Client = IN3.default
const apis = {}
function hasAPI(api) {
    if (apis[api] === undefined) {
        const c = new IN3()
        apis[api] = !!c[api]
        c.free();
    }
    return apis[api]
}

require('mocha')
const { assert } = require('chai')
const testDir = '../../c/test/testdata/requests'
if (process.argv.find(_ => _.indexOf('mocha') >= 0)) {

    describe('JSON-Tests', () => {

        for (const f of fs.readdirSync(testDir)) {
            it(f, async () => {
                const all = await run_test([testDir + '/' + f], -1)
                for (const r of all)
                    assert.isTrue(r.success, r.c + ' : ' + r.descr + ' failed : ' + r.error)
            })
        }
    })
}

const ignoreFuxxProps = ['id', 'error', 'code', 'dap', 'weight', 'confirmations', 'version', 'proofHash', 'strippedsize', 'height', 'difficulty', 'nTx', 'mediantime', 'registryId', 'timeout', 'lastBlockNumber', 'lastWhiteList', 'currentBlock', 'rpcTime', 'rpcCount', 'gasUsed', 'execTime', 'lastNodeList', 'totalDifficulty', 'size', 'chainId', 'transactionLogIndex', 'logIndex', 'lastValidatorChange']
const ignoreTxProps = ['from', 'blockHash', 'blockNumber', 'publicKey', 'raw', 'standardV', 'transactionIndex']
const ignoreVoutProps = ['value', 'reqSigs']


async function runFuzzTests(filter, test, allResults, c, ob, prefix = '') {
    if (!ob) return c
    for (const k of Object.keys(ob).filter(_ => _
        && ignoreFuxxProps.indexOf(_) < 0
        && (prefix.indexOf('proof.transactions') < 0 || ignoreTxProps.indexOf(_) < 0)
        && (prefix.indexOf('result.vout') < 0 || ignoreVoutProps.indexOf(_) < 0)
    )) {
        if (k === 'txIndex' && test.response[0].result === null)
            continue
        const val = ob[k]
        if (typeof val === 'string') {
            if (val.startsWith('0x')) {
                if (val.length == 2) ob[k] = '0x01'
                else if (val[2] === '9') ob[k] = '0xa' + val.substr(3)
                else if (val[2].toLowerCase() === 'f') ob[k] = '0x0' + val.substr(3)
                else ob[k] = '0x' + String.fromCharCode(val[2].charCodeAt(0) + 1) + val.substr(3)
            }
            else continue
        }
        else if (typeof val === 'number')
            ob[k] = val + 1
        else if (Array.isArray(val)) {
            if (val[0] && typeof val[0] === 'object') c = await runFuzzTests(filter, test, allResults, c, val[0], prefix + '.' + k)
            continue
        }
        else if (typeof val === 'object') {
            c = await runFuzzTests(filter, test, allResults, c, val, prefix + '.' + k)
            continue
        }
        else continue

        c++
        if (filter < 0 || c == filter) {
            test.success = false
            const result = await runSingleTest(test, c)
            test.success = true
            allResults.push(result)
            console.log(addSpace('' + result.c, 3) + ' : ' + addSpace('  ' + prefix + '.' + k, 85, '.', result.success ? '' : '31') + ' ' + addSpace(result.success ? 'OK' : result.error, 0, ' ', result.success ? '32' : '31'))
        }
        ob[k] = val
    }

    return c
}



async function run_test(files, filter) {
    const allResults = []
    let c = 0
    for (const file of files) {
        for (const test of JSON.parse(fs.readFileSync(file, 'utf8'))) {
            if (test.api && !hasAPI(test.api)) continue
            c++
            if (filter < 0 || c == filter) {
                const result = await runSingleTest(test, c)
                allResults.push(result)
                console.log(addSpace('' + result.c, 3) + ' : ' + addSpace(result.descr, 85, '.', result.success ? '' : '31') + ' ' + addSpace(result.success ? 'OK' : result.error, 0, ' ', result.success ? '32' : '31'))
            }

            if (test.fuzzer)
                c = await runFuzzTests(filter, test, allResults, c, test.response[0])
        }
    }
    return allResults
}

async function runSingleTest(test, c) {
    test = JSON.parse(JSON.stringify(test))
    let res = test.intern ? 1 : 0
    const config = test.config || {}, result = { descr: test.descr, c, success: false, error: undefined }
    let accounts = {}

    Client.setStorage({
        get: _ => {
            if (accounts && _.startsWith('C')) {
                let ac = accounts['0x' + _.substr(1)]
                if (!ac)
                    Object.keys(accounts).forEach(_ => accounts[_.toLowerCase()] = accounts[_])
                ac = accounts['0x' + _.substr(1)]
                if (ac && ac.code)
                    return ac.code.substr(2)
            }
            return null
        }, set: _ => { }
    })
    Client.setTransport((url, data) => {
        /*
        if ((data as any)[0].method == 'in3_validatorlist') {
            const response = JSON.parse(readFileSync(process.cwd() + '/test/util/in3_validatorlist_' + test.chainId + '.json', 'utf8').toString())
            const validatorResponse = mockValidatorList(response, (data as any)[0].params)

            validatorResponse.id = (data as any)[0].id
            validatorResponse.jsonrpc = (data as any)[0].jsonrpc

            return Promise.resolve([validatorResponse])
        }
        */
        if (test.response.length <= res) return Promise.reject(new Error('Not enought responses!'))
        test.response[res].id = data[0].id
        const r = test.response[res++]
        accounts = r.in3 && r.in3.proof && r.in3.proof.accounts
        const json = JSON.stringify([r])
        //        console.log('RES:', json.substr(0, 20))
        return Promise.resolve(json)
    })
    const client = new Client({
        requestCount: config.requestCount || 1,
        autoUpdateList: false,
        includeCode: true,
        bootWeights: false,
        experimental: true,
        proof: test.proof || 'standard',
        maxAttempts: 1,
        finality: test.finality || 0,
        signatureCount: test.signatures ? test.signatures.length : 0,
        nodeRegistry: {
            needsUpdate: false
        }
    })
    await client.setConfig({ chainId: test.chainId || '0x1' })

    let s = false, error = null
    try {
        const response = await client.send(test.request)
        if (test.intern && JSON.stringify(response.result) != JSON.stringify(test.response[0].result))
            throw new Error('wrong result: actual:' + JSON.stringify(response.result) + 'should:' + JSON.stringify(test.response[0].result))
        s = !!(response && response.result !== undefined)
    }
    catch (err) {
        //        console.log(err.stack)
        error = err
    }
    client.free()
    if (s === (test.success == undefined ? true : test.success))
        result.success = true
    else
        result.error = s ? 'Should have failed' : (error && error.message) || 'Failed'
    return result
}

function addSpace(s, l, filler = ' ', color = '') {
    while (s.length < l) s += filler
    return color ? '\x1B[' + color + 'm' + s + '\x1B[0m' : s
}

if (!process.argv.find(_ => _.indexOf('mocha') >= 0)) {
    let filter = -1;
    const files = []
    for (const a of process.argv.slice(2)) {
        if (a == '-t') filter = -2
        else if (filter === -2)
            filter = parseInt(a)
        else if (a.indexOf('.json') != -1)
            files.push(a)
    }
    //console.log("files:", JSON.stringify(files))
    run_test(files, filter).then(() => console.log('done'), console.log)
}
