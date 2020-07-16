# jsock

Key-value-based, HMAC-signed, non-blocking sockets for Python

## Installation


## Usage

Please check `example.py`.


## Serializer/deserializer Benchmark

Check `benchmark.py`.

- json:
  - send: 60005.29 op/s
  - recv: 79790.10 op/s
  - total time: 1.459s
- simplejson:
  - send: 50552.37 op/s
  - recv: 83004.80 op/s
  - total time: 1.591s
- msgpack:
  - send: 93561.46 op/s
  - recv: 145995.07 op/s
  - total time: 0.877s
- pickle:
  - send: 87664.16 op/s
  - recv: 136931.65 op/s
  - total time:  0.935s

