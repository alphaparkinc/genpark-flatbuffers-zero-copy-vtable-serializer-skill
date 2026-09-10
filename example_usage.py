from client import FlatBuffersSerializer

def main():
    print("=== Testing FlatBuffers Zero-Copy Serializer ===")
    fb = FlatBuffersSerializer()
    buf = fb.serialize([(0, 100), (1, 250)])
    print("Serialized binary length:", len(buf))

    v0 = fb.read_field(buf, 0)
    v1 = fb.read_field(buf, 1)
    print(f"Direct read field 0 => {v0}, field 1 => {v1}")

    assert v0 == 100 and v1 == 250
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
