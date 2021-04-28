# Version 1.1.3
- Async cloud evaluator based on `aiohttp` now use `certifi` to create a default `SSLContext` if none is provided. Other cloud evaluator are based on the `requests` module which also uses this library. 
- Updating dependency list accordingly in `setup.py`. `certifi` was already listed as a `requests` dependency, so this should have no direct impact on user site package.
# Version 1.1.3
- Update asynchronous evaluator classes. Remove the `loop` parameter. Most optional loop parameters are deprecated in the Python standart library `asyncio` and in most libraries, mainly because it is misleading and lead to misuses and bugs. The loop parameter is useful when instantiating asynchronous evaluators outside the scope of an event loop. It's implementation was not good enough and was relying on usages deprecated in 3.8.
- Removing four asynchronous generators in asynchronous evaluation result classes: `iter_messages`, `iter_messages_name`, `iter_messages_tuple` and `iter_output`. These coroutines are only working on python 3.6+ and are not critical enough to drop support for 3.5. Asynchronous properties: `messages`, `messages_name` and `output` provide the same information.

# Version 1.1.2
- Fix a backward incompatible change introduced in 12.1. Make sure the library works with any kernel version starting with 11.3.
- Minor changes and tweaks.

# Version 1.1.0
- WXF deserialization maps `List` to `tuple`, was `list` before for two reasons. `List` and tuple are immutable. `tuple` contrary to `list` are hashable object and as such can be keys in `dict`.
- WXF deserialization maps numeric arrays to `NumPy` arrays. Numpy being a pre-requisite of the library, and lazily loaded, this change will boost performances while causing very little trouble, if any.
- Fix bug in `WolframLanguageSession` that was preventing Python interpreter from exiting.
- Add new class `PackedArray`, a wrapper on top of NumPy `ndarray`. Instances of `PackedArray` are serialized as... WL packed array (!). This fixes the issue of having a WL packed array (say the output of `Range[3]`), being serialized to a `ndarray` (`arange(3)`), and send back to the kernel as a `NumericArray`. 
- Use `black` code formatter.

# Version 1.0.2
- Add two new optional flags to `test` command called `-x` or `--xml` and `-d` or `--xml-dir`. It produces an xml output of the test results using the `unittest-xml-reporting` library. `-d` expects the filepath of the output directory, default is `test-reports`. Also add `-v` or `--verbosity` to control the `verbosity` option of the test suite. Check `python run.py test -h` for more info.

# Version 1.0.1
- Bug fix in `WXFConsumer`.
- Update some URLs.

# Version 1.0.0
- Introducing a new class `WolframKernelController`. Major code change to ensure ZMQ sockets are isolated in a given thread. Add a new controller class, a `Thread`, that own the sockets connected to the kernel. Interaction with this thread is done through a Queue.
- Merge `WolframLanguageFutureSession` into `WolframLanguageSession`. All evaluate methods have a future counterpart.
- Merge `WolframCloudFutureSession` into `WolframCloudSession`. Add relevant future methods.
- Rename `WolframAPICall` method `add_parameter` to `set_parameter` since setting is exactly what it does.
- Result of API call, the `WolframAPIResponse` family of classes, now automatically deserialize the response content using the content-type, if it's `WXF` or `JSON`. The content type remains accessible in the `response` member of those classes.
- rename evaluator parameters `STARTUP_READ_TIMEOUT` to `STARTUP_TIMEOUT`, and `TERMINATE_READ_TIMEOUT` to `TERMINATE_TIMEOUT`.
- CPU consumption reduced to ~1% with the latest ZMQLink version.
- Local session checks for the Wolfram Kernel version at startup and fails with a specific message.
- Local session supports instant logging for messages, with severity `warn`, and prints, with severity `info`. This only works for kernel with a `kernel_loglevel` set on initialization, and allows real time feedbacks, even if the kernel evaluation is not yet completed.
- Change mapping of WXF symbols to Python objects. The only symbols that are deserialized to Python objects are the one that round trips: `Null`, `True`, `False`. `Pi` and `None` are no more deserialized to, respectively, `math.pi` and `None`.

# Version 1.0.0.dev4
- Inconsistent class name `WolframCloudSessionFuture` replaced with `WolframCloudFutureSession`.
- Rework completely `Dispatch` class. Add a `Dispatch` instance called `wolfram_encoder` representing the multi dispatch function that encodes Python object.
- Add an entry point allowing new encoders to be registered as separated libraries (plugins).
- Add support for pandas classes: `Series` and `DataFrame`.
- Extend support for NumPy numbers.
- Local evaluators can be initialized without a Wolfram Kernel path, in which case default paths are scanned to find the most recent product.

# Version 1.0.0.dev3
- Add `CHANGELOG.md` to the repository to help users track the changes.
- Major refactoring of the evaluation module.
    - add base classes for synchronous and asynchronous evaluation, specifying the evaluation scheme.
    - add cloud session implementation based on event loop using the aiohttp library.
    - rename asynchronous session based on future module from `WolframCloudAsyncSession` to `WolframCloudSessionFuture`.
    - add new implementation of `WolframCloudAsyncSession` based on asyncio and coroutines.
- Cloud session named option `authentication` renamed `credentials`.
- Significant improvement of `PIL.Image` support. Speed up serialization and deserialization of images, and add support for more input formats.

# Version 1.0.0.dev2
First released version of the library as a release candidate.