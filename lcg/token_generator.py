
class token_stream:

    def __init__(self, seed: int, multiplier: int, increment: int, modulus: int):
        self._seed = seed
        self._multiplier = multiplier
        self._increment = increment
        self._modulus = modulus
        self._n_state = 3
        self.tokens = generate_tokens(self._seed, self._multiplier, self._increment, self._modulus)

    def __contains__(self, token: int):
        return token in self.tokens

    def regenerate_active_tokens(self):
        self._n_state += 3
        self.tokens = generate_tokens(self.tokens[2], self._multiplier, self._increment, self._modulus)




def generate_tokens(seed: int, multiplier: int, increment: int, modulus: int) -> list[int]:
    tokens: list[int] = []  

    current_state: int = seed

    for i in range(3):
        current_state = (multiplier * current_state + increment) % modulus
        tokens.append(current_state)

    return tokens





stream = token_stream(0, 3, 1, 8)

print("yes" if 1 in stream else "no")
print(stream.tokens)
stream.regenerate_active_tokens()
print(stream.tokens)
print("yes" if 3 in stream else "no")

