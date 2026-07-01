class GuardrailService:

    def is_wellness_related(
        self,
        message: str
    ):

        message = message.lower()

        blocked_keywords = [

            "python",
            "java",
            "c++",
            "javascript",
            "html",
            "css",
            "sql",

            "math",
            "equation",
            "calculate",
            "solve",
            "algebra",

            "physics",
            "chemistry",

            "homework",
            "assignment",

            "programming",
            "coding",

            "algorithm",
            "data structure"
        ]

        for keyword in blocked_keywords:

            if keyword in message:

                return False

        return True