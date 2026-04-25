# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class LanguageDetector(gl.Contract):
    last_language: str
    total_detected: u256

    def __init__(self) -> None:
        self.last_language = "none"
        self.total_detected = u256(0)

    @gl.public.write
    def detect(self, text: str) -> None:
        prompt = f"""What language is this text written in?
        Text: {text}
        Reply with the language name only. Example: English, French, Arabic"""

        def leader_fn():
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_language = str(result).strip()
        self.total_detected = self.total_detected + u256(1)

    @gl.public.view
    def get_language(self) -> str:
        return self.last_language

    @gl.public.view
    def get_total(self) -> u256:
        return self.total_detected
