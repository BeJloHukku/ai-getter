
class AIGetterBaseError(Exception):
    pass


class AiGeminiError(AIGetterBaseError):
    pass


class NoResponseWasGivenFromGeminiError(AIGetterBaseError):
    pass

