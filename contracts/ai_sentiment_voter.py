# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class SentimentVoter(gl.Contract):
    result: str
    total_votes: u256

    def __init__(self) -> None:
        self.result = "none"
        self.total_votes = u256(0)

    @gl.public.write
    def vote(self, text: str) -> None:
        prompt = f"""Analyze sentiment of this text.
        Text: {text}
        Reply one word only: positive, negative, or neutral"""

        def leader_fn():
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.result = str(result).strip().lower()
        self.total_votes = self.total_votes + u256(1)

    @gl.public.view
    def get_result(self) -> str:
        return self.result

    @gl.public.view
    def get_total(self) -> u256:
        return self.total_votes
