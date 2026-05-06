import magic
try:
    m = magic.Magic(mime=True)
    print(f"Magic works! MIME type: {m.from_buffer(b'test')}")
except Exception as e:
    print(f"Magic failed: {e}")
    import traceback
    traceback.print_exc()
