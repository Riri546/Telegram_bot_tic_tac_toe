from typing import Union


class String(str):
    def __new__(cls, string: str): return super().__new__(cls, string)

    @property
    def normal(self) -> str:
        """
        Returns a string without special characters: ,.-;:_´ç`+¨Ç^*{}[]ºª!\"·$%&/()=?¿<>\\|@#~€¬

        :return:
        """

        return self.remove_chars()

    def get_chars(self, number_of_chars: int = 1) -> list:
        """
        Returns a list with the number of characters selected starting from the beginning
        If the number_of_chars is higher than the lenth of the string, it will return all the string characters

        :param number_of_chars:
        :return:
        """

        return "".join(self.asList()[:number_of_chars])

    def get_chars_reversed(self, number_of_chars: int = 1) -> list:
        """
        Returns a list with the number of characters selected starting from the end
        If the number_of_chars is higher than the lenth of the string, it will return all the string characters

        :param number_of_chars:
        :return:
        """

        return "".join(list(self.asList().__reversed__())[:number_of_chars])

    def remove_chars(self, characters: list = None) -> str:
        """
        Returns a string without characters in custom list

        :param characters:
        :return:
        """

        special_chars = characters if characters else [char for char in ",.-;:_´ç`+¨Ç^*{}[]ºª!\"·$%&/()=?¿<>\\|@#~€¬"]

        result = []
        for word in self.strip("".join(special_chars)).split():
            for char in special_chars:
                word = word.replace(char, "")

            result.append(word)

        return " ".join(result)

    def asList(self) -> list:
        """
        Returns string as list object

        :return:
        """

        return [char for char in self]

    def asBytes(self, encoding: str = "UTF-8") -> bytes:
        """
        Returns string as bytes object with custom encoding

        :param encoding:
        :return:
        """

        return bytes(self, encoding)

    def isPalindrome(self) -> bool:
        """
        Returns whether or not the given string is a palindrome

        :return:
        """

        return self == self.__reversed__()

    def isPlural(self) -> bool:
        """
        Returns a list with all stripped words from the string as True or False, depending on whether the given word is plural or not

        string = "hello my name is Plural, and yours?"
        string_returned = [False, False, False, True, False, False, True]

        :return:
        """

        return [word[-1] == "s" or word[:-3:-1] == "se" for word in self.normal.split()]

    def isSingular(self) -> bool:
        """
        Returns a list with all stripped words from the string as True or False, depending on whether the given word is singular or not

        string = "hello my name is Singular, and yours?"
        string_returned = [True, True, True, False, True, True, False]

        :return:
        """

        return [not plural for plural in self.isPlural()]


class Analyzer(String):
    def __new__(cls, string: str): return super().__new__(cls, string)

    def differences(self, string: Union[str, String]) -> list:
        """
        Returns a list with all the differences between the passed string
        It uses the zip function, so if the length of one string is greater than the other, the values that exceed will be ignored

        ** It is planned to change it in the future

        return = {
                "index": 0,
                "word": "hello",
                "word2": "bye"
        }

        :param string:
        :return:
        """

        return [
            {
                "index": index,
                "word": word,
                "word2": word_
            }
            for index, words in enumerate(zip(self.split(), string.split()))
            if (word := words[0]) != (word_ := words[-1])
        ]

    def consecutives(self, separator: Union[str, String]) -> list:
        """
        Returns a list with all the words that has consecutive characters equal to the separator

        string = "hello my name is Plural, and yours?"
        separator = "l"
        string_returned =  True ( hello has consecutive "l" )

        :param separator:
        :return:
        """

        result = []
        char_before = ""

        for char in self:
            result.append(char == char_before and char == separator)
            char_before = char

        return result

    def hasDifferences(self, string: Union[str, String]) -> bool:
        """
        Returns if the string has differences from the string passed.

        :param string:
        :return:
        """

        return any(self.differences(string))

    def hasConsecutive(self, separator: Union[str, String]) -> bool:
        """
        Returns if the string has two or more consecutive characters equal to the separator

        :param separator:
        :return:
        """

        return any(self.consecutives(separator))
