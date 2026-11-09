from rsa.rsa_types import *
from lcg.token_generator import *
import json
import sys

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

    args = sys.argv[1:]

    try:
        if "-f" in args:
            if len(args) < 2:
                raise RuntimeError("Invalid Arguments, must use: -f {filename}")

            with open(args[args.index("-f") + 1], "r") as json_file:
                rsa_input_fields: str = ["first_prime", "second_prime", "public_exponent"]
                lcg_input_fields: str = ["seed", "multiplier", "increment", "modulus"]
                test_payload_fields: str = ["student_id", "test_token"]
                fields: str = rsa_input_fields + lcg_input_fields + test_payload_fields
                json_data = json.load(json_file)

                missing_fields = [key for key in fields if key not in json_data]

                if missing_fields:
                    raise KeyError(f"Fields not set in json file: {missing_fields}")


                key_generation_results = {key: json_data[key] for key in rsa_input_fields}
                pub_key, priv_key = generate_keys(json_data[rsa_input_fields[0]], json_data[rsa_input_fields[1]], json_data[rsa_input_fields[2]])
                key_generation_results |= {"public_key": [pub_key.exponent, pub_key.modulus], "private_key": [priv_key.exponent, priv_key.modulus]}


                token_generation_results = {key: json_data[key] for key in lcg_input_fields}
                token_generator: token_stream = token_stream(json_data[lcg_input_fields[0]], json_data[lcg_input_fields[1]], json_data[lcg_input_fields[2]], json_data[lcg_input_fields[2]])
                token_generation_results |=  {"active_tokens": token_generator.tokens}
                
                test_results = {key: json_data[key] for key in test_payload_fields}
                encrypted_id = encrypt(pub_key, json_data[test_payload_fields[0]])
                test_results |= {"encrypted_data": encrypted_id, "decrypted_data": decrypt(priv_key, encrypted_id), "token_auth_results": "Authenticated" if json_data["test_token"] in token_generator else "Unauthenticated"}

                #Tinulad ko latta style mon ah
                print("======================")
                print("RSA RESULTS")
                print("======================")
                print_dict(key_generation_results)

                print("======================")
                print("LCG RESULTS")
                print("======================")
                print_dict(token_generation_results)


                print("======================")
                print("ENCRYPTION AND VERIFICATION TEST RESULTS")
                print("======================")
                print_dict(test_results)

                return



    
            

    except Exception as e:
        print(str(e))
        return
    






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