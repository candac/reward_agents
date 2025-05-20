import re
from .agent_base import AgentBase

class Planner(AgentBase):
    tools_desps = [
        {
            "name": "constraint check",
            "desp": "A 'constraint check' is required if the instruction contains any additional constraints or requirements on the output, such as length, keywords, format, number of sections, frequency, order, etc.",
            "identifier": "[[A]]"
        },
        {
            "name": "factuality check",
            "desp": "A 'factuality check' is required if the generated response to the instruction potentially contains claims about factual information or world knowledge.",
            "identifier": "[[B]]"
        }
    ]

    @staticmethod
    def build_prompt(instruction: str) -> str:
        return (
            "You are an intelligent planner. Decide which specialised verification "
            "checks are NECESSARY for the user instruction.\n"
            "A 'constraint check' is required if the instruction contains any additional constraints or requirements on the output,such as length, keywords, format, number of sections, frequency, order, etc.\n"
            "A 'factuality check' is required if the generated response to the instruction potentially contains claims about factual information or world knowledge.\n\n"
            f"[Instruction]\n{instruction.strip()}\n\n"
            f"[Available checks]\n{Planner.tools_desps}\n\n"
            "If checks are needed, output ONLY their identifiers, comma-separated "
            "(e.g. [[A]],[[B]]). If none are needed, output [[NONE]]."
        )

    _ident_re = re.compile(r"\[\[([A-Z]+)\]\]")

    def __call__(self, instruction: str):
        prompt = self.build_prompt(instruction)
        reply = self.chat_completion(
            messages=[{"role": "user", "content": prompt}],
        ) 
        #print(f"[Planner] Model raw reply: {reply!r}") # uncomment to see raw reply from LLM
        lines = reply.strip().splitlines()
        last_tag_line = None
        for line in reversed(lines):
            if self._ident_re.search(line):
                last_tag_line = line
                break
        if last_tag_line is None:
            return []
        tags = self._ident_re.findall(last_tag_line)
        return list(dict.fromkeys(tags))
