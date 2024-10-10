# from cryptography.hazmat.primitives import hashes

# def calculate_file_hash(file_path) -> str:
#     """MD5 encoding file to hex string 32bytes"""
#     with open(file_path, "rb") as f:
#         file_hash = hashes.Hash(hashes.MD5())
#         while chunk := f.read(4096):
#             file_hash.update(chunk)
#         return file_hash.finalize().hex()

# def main():
#     file_path1 = "/home/default/file_upload/Process"
#     file_path2 = "/home/default/file_upload/test1"
#     file_path3 = "/home/default/file_upload/test2"
#     print(calculate_file_hash(file_path1))
#     print(calculate_file_hash(file_path2))
#     print(calculate_file_hash(file_path3))


# if __name__ == '__main__':
#     main()
