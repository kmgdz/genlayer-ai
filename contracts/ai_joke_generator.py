# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class JokeGenerator(gl.Contract):
    last_joke: str
    total_jokes: u256

    def __init__(self) -> None:
        self.last_joke = "none"
        self.total_jokes = u256(0)

    @gl.public.write
    def generate(self, topic: str) -> None:
        prompt = f"""Tell me a short funny joke about: {topic}
        Keep it under 2 sentences. Be creative."""

        def leader_fn():
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_joke = str(result).strip()
        self.total_jokes = self.total_jokes + u256(1)

    @gl.public.view
    def get_joke(self) -> str:
        return self.last_joke

    @gl.public.view
    def get_total(self) -> u256:
        return self.total_jokes
