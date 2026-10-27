from rsa.rsa_types import *
from lcg.token_generator import *
import json

def integer_input(msg: str) -> int:
    while True:
        try:
            temp: int = int(input(msg))
            return temp
        except ValueError:
            print("Invalid Input!!!")
            continue

def print_dict(dict):
    for key,val in dict.items():
        print(f"{key}: {val}")

def main():

    while True:
        try:  
            rsa_vals = {}

            print("======================")
            print("RSA PARAMETERS")
            print("======================")
            rsa_vals["p"] = integer_input("First prime: ")
            rsa_vals["q"] = integer_input("Second prime: ")
            rsa_vals["public_exponent"] = integer_input("Public exponent: ")

            public_key, private_key = generate_keys(rsa_vals["p"],
                                                    rsa_vals["q"], rsa_vals["public_exponent"])

            rsa_vals["public_key"] = public_key.exponent, public_key.modulus
            rsa_vals["private_key"] = private_key.exponent, private_key.modulus

            lcg_vals = {}
            print("======================")
            print("LCG PARAMETERS")
            print("======================")
            lcg_vals["seed"] = integer_input("seed: ")
            lcg_vals["multiplier"] = integer_input("multiplier: ")
            lcg_vals["increment"] = integer_input("increment: ")
            lcg_vals["modulus"] = integer_input("modulus: ")

            
            tk_stream = token_stream(lcg_vals["seed"],
                                lcg_vals["multiplier"],
                                lcg_vals["increment"],
                                lcg_vals["modulus"])
            
            lcg_vals["active_tokens"] = tk_stream.tokens


            payload_vals = {}
            print("======================")
            print("PAYLOAD")
            print("======================")
            payload_vals["student_id"] = input("Student ID: ")
            payload_vals["challenge_token"] = integer_input("Input challenge token (must be int): ")

            result_vals = {}
            result_vals["encrypted_id"] = encrypt(public_key, payload_vals["student_id"])
            result_vals["unencrypted_id"] = decrypt(private_key, result_vals["encrypted_id"])
            result_vals["passed_token_verification"] = payload_vals["challenge_token"] in tk_stream


            print("======================")
            print("RSA RESULTS")
            print("======================")
            print_dict(rsa_vals)


            print("======================")
            print("LCG RESULTS")
            print("======================")
            print_dict(lcg_vals)



            print("======================")
            print("ENCRYPTION AND VERIFICATION TEST RESULTS")
            print("======================")
            print_dict(payload_vals)
            print_dict(result_vals)


            return


        
        except Exception as e:
            print()
            print(f"Error: {e}")
            print()





if __name__ == "__main__":
    main()