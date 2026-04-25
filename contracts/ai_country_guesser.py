# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class CountryGuesser(gl.Contract):
    last_country: str
    last_hint: str
    total_guesses: u256

    def __init__(self) -> None:
        self.last_country = "none"
        self.last_hint = "none"
        self.total_guesses = u256(0)

    @gl.public.write
    def guess(self, hint: str) -> None:
        prompt = f"""Based on this hint, what country am I describing?
        Hint: {hint}
        Reply with the country name only."""

        def leader_fn():
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_country = str(result).strip()
        self.last_hint = hint
        self.total_guesses = self.total_guesses + u256(1)

    @gl.public.view
    def get_country(self) -> str:
        return self.last_country

    @gl.public.view
    def get_total(self) -> u256:
        return self.total_guesses
