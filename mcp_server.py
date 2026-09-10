import sys
import json
import base64
from client import FlatBuffersSerializer

def main():
    fb = FlatBuffersSerializer()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        req = json.loads(line)
        method = req.get("method")
        params = req.get("params", {})
        if method == "serialize":
            fields = [(f.get("id"), f.get("val")) for f in params.get("fields", [])]
            buf = fb.serialize(fields)
            res = {"bytes_b64": base64.b64encode(buf).decode()}
        elif method == "read_field":
            raw = base64.b64decode(params.get("bytes_b64", "").encode())
            val = fb.read_field(raw, params.get("field_id", 0))
            res = {"value": val}
        else:
            res = {"error": "unknown method"}
        sys.stdout.write(json.dumps({"id": req.get("id"), "result": res}) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
