# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class AITranslator(gl.Contract):
    last_translation: str
    total_translations: u256

    def __init__(self) -> None:
        self.last_translation = "none"
        self.total_translations = u256(0)

    @gl.public.write
    def translate(self, text: str, language: str) -> None:
        prompt = f"""Translate this text to {language}:
        Text: {text}
        Reply with the translation only."""

        def leader_fn():
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            return True

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        self.last_translation = str(result).strip()
        self.total_translations = self.total_translations + u256(1)

    @gl.public.view
    def get_translation(self) -> str:
        return self.last_translation

    @gl.public.view
    def get_total(self) -> u256:
        return self.total_translations
