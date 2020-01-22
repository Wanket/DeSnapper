class Cleanup(int):
    __create_key__ = object()

    __cleanup_int_to_str = {
        0: "",
        1: "number",
        2: "timeline",
        3: "empty-pre-post"
    }

    __cleanup_str_to_int = {value: key for key, value in __cleanup_int_to_str.items()}

    @staticmethod
    def from_str(cleanup: str) -> int:
        return Cleanup(Cleanup.__cleanup_str_to_int[cleanup])

    def __str__(self):
        return Cleanup.__cleanup_int_to_str[self]