import msgpack

def pack(obj):
    return msgpack.packb(obj, encoding='utf-8')

def unpack(obj):
    return msgpack.unpackb(obj, encoding='utf-8')
