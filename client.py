class FlatBuffersSerializer:
    """
    FlatBuffers Zero-Copy Table Serializer.
    Enables instant field access via offset vtables without buffer unpacking.
    """
    def serialize(self, fields):
        vtable = [len(fields) * 2 + 4, 4 + len(fields) * 4]
        offset = 4
        for fid, val in fields:
            vtable.append(offset)
            offset += 4

        data = bytearray()
        vtable_bytes = bytearray()
        for v in vtable:
            vtable_bytes.extend(v.to_bytes(2, "little"))

        for fid, val in fields:
            data.extend(val.to_bytes(4, "little"))

        return bytes(vtable_bytes + data)

    def read_field(self, buffer, field_id):
        vtable_len = int.from_bytes(buffer[0:2], "little")
        offset_in_vtable = 4 + field_id * 2
        if offset_in_vtable >= vtable_len:
            return None
        field_offset = int.from_bytes(buffer[offset_in_vtable:offset_in_vtable+2], "little")
        data_pos = vtable_len + field_offset - 4
        return int.from_bytes(buffer[data_pos:data_pos+4], "little")
