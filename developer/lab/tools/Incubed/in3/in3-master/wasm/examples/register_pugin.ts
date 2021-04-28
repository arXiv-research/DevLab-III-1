// Register a custom RPC for sha256 hashing using a plugin
// Read about IN3 Plugins in the docs: https://in3.readthedocs.io/en/develop/api-c.html#plugins
import { IN3, RPCRequest, IN3Plugin } from 'in3'
import * as crypto from 'crypto'

class Sha256Plugin<BigIntType, BufferType> implements IN3Plugin<BigIntType, BufferType> {

  // this function will register for handling rpc-methods
  // only if we return something other then `undefined`, it will be taken as the result of the rpc.
  // if we don't return, the request will be forwarded to the IN3 nodes
  handleRPC(client, request: RPCRequest): any {

    if (request.method === 'sha256') {
      // assert params
      if (request.params.length != 1 || typeof (request.params[0]) != 'string')
        throw new Error('Only one parameter with as string is expected!')

      // create hash
      const hash = crypto.createHash('sha256').update(Buffer.from(request.params[0], 'utf8')).digest()

      // return the result
      return '0x' + hash.toString('hex')
    }
  }

}

async function registerPlugin() {

  // create new IN3 instance
  const client = new IN3()

  // register the plugin
  client.registerPlugin(new Sha256Plugin())

  // exeucte a rpc-call
  const result = await client.sendRPC("sha256", ["testdata"])

  console.log(" sha256: ", result)

}

registerPlugin().catch(console.error)
