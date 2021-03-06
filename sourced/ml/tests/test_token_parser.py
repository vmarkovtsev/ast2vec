import pickle
import unittest

from sourced.ml.algorithms import NoopTokenParser, TokenParser


class TokenParserTests(unittest.TestCase):
    def setUp(self):
        self.tp = TokenParser(stem_threshold=4, max_token_length=20, attach_upper=False)
        self.tp._single_shot = False

    def test_process_token(self):
        self.tp.max_token_length = 100

        tokens = [
            ("ONLYCAPS", ["onlycap"]),
            ("nocaps", ["nocap"]),
            ("UpperCamelCase", ["upper", "camel", "case"]),
            ("camelCase", ["camel", "case"]),
            ("FRAPScase", ["frap", "case"]),
            ("SQLThing", ["sqlt", "hing"]),
            ("_Astra", ["astra"]),
            ("CAPS_CONST", ["caps", "const"]),
            ("_something_SILLY_", ["someth", "silli"]),
            ("blink182", ["blink"]),
            ("FooBar100500Bingo", ["foo", "bar", "bingo"]),
            ("Man45var", ["man", "var"]),
            ("method_name", ["method", "name"]),
            ("Method_Name", ["method", "name"]),
            ("101dalms", ["dalm"]),
            ("101_dalms", ["dalm"]),
            ("101_DalmsBug", ["dalm", "bug"]),
            ("101_Dalms45Bug7", ["dalm", "bug"]),
            ("wdSize", ["wd", "size", "wdsize"]),
            ("Glint", ["glint"]),
            ("foo_BAR", ["foo", "bar"]),
            ("sourced.ml.algorithms.uast_ids_to_bag",
             ["sourc", "sourcedml", "algorithm", "mlalgorithm",
              "uast", "ids", "idsto", "bag", "tobag"]),
            ("WORSTnameYOUcanIMAGINE", ["worst", "name", "you", "can", "imagin"]),
            # Another bad example. Parser failed to parse it correctly
            ("SmallIdsToFoOo", ["small", "ids", "idsto", "fo", "oo"]),
            ("SmallIdFooo", ["small", "smallid", "fooo", "idfooo"]),
            ("ONE_M0re_.__badId.example", ["one", "onem", "re", "bad", "rebad",
                                           "badid", "exampl", "idexampl"]),
            ("never_use_Such__varsableNames", ["never", "use", "such", "varsabl", "name"]),
            ("a.b.c.d", ["a", "b", "c", "d"]),
            ("A.b.Cd.E", ["a", "b", "cd", "e"]),
            ("looong_sh_loooong_sh", ["looong", "looongsh", "loooong", "shloooong", "loooongsh"]),
            ("sh_sh_sh_sh", ["sh", "sh", "sh", "sh"]),
            ("loooong_loooong_loooong", ["loooong", "loooong", "loooong"])
        ]

        for token, correct in tokens:
            res = list(self.tp.process_token(token))
            self.assertEqual(res, correct)

    def test_process_token_with_attach_upper(self):
        tp = TokenParser(stem_threshold=100, single_shot=True, max_token_length=100,
                         min_split_length=1)
        tokens = [
            ("ONLYCAPS", ["onlycaps"]),
            ("nocaps", ["nocaps"]),
            ("UpperCamelCase", ["upper", "camel", "case"]),
            ("camelCase", ["camel", "case"]),
            ("FRAPScase", ["frap", "scase"]),
            ("SQLThing", ["sql", "thing"]),
            ("_Astra", ["astra"]),
            ("CAPS_CONST", ["caps", "const"]),
            ("_something_SILLY_", ["something", "silly"]),
            ("blink182", ["blink"]),
            ("FooBar100500Bingo", ["foo", "bar", "bingo"]),
            ("Man45var", ["man", "var"]),
            ("method_name", ["method", "name"]),
            ("Method_Name", ["method", "name"]),
            ("101dalms", ["dalms"]),
            ("101_dalms", ["dalms"]),
            ("101_DalmsBug", ["dalms", "bug"]),
            ("101_Dalms45Bug7", ["dalms", "bug"]),
            ("wdSize", ["wd", "size"]),
            ("Glint", ["glint"]),
            ("foo_BAR", ["foo", "bar"]),
            ("sourced.ml.algorithms.uast_ids_to_bag",
             ["sourced", "ml", "algorithms", "uast", "ids", "to", "bag"]),
            ("WORSTnameYOUcanIMAGINE", ["wors", "tname", "yo", "ucan", "imagine"]),
            # Another bad example. Parser failed to parse it correctly
            ("SmallIdsToFoOo", ["small", "ids", "to", "fo", "oo"]),
            ("SmallIdFooo", ["small", "id", "fooo"]),
            ("ONE_M0re_.__badId.example", ["one", "m", "re", "bad",
                                           "id", "example"]),
            ("never_use_Such__varsableNames", ["never", "use", "such", "varsable", "names"]),
            ("a.b.c.d", ["a", "b", "c", "d"]),
            ("A.b.Cd.E", ["a", "b", "cd", "e"]),
            ("looong_sh_loooong_sh", ["looong", "sh", "loooong", "sh"]),
            ("sh_sh_sh_sh", ["sh", "sh", "sh", "sh"]),
            ("loooong_loooong_loooong", ["loooong", "loooong", "loooong"])
        ]

        for token, correct in tokens:
            res = list(tp.process_token(token))
            self.assertEqual(res, correct)

    def test_process_token_single_shot(self):
        self.tp.max_token_length = 100
        self.tp._single_shot = True
        self.tp.min_split_length = 1
        tokens = [
            ("ONLYCAPS", ["onlycap"]),
            ("nocaps", ["nocap"]),
            ("UpperCamelCase", ["upper", "camel", "case"]),
            ("camelCase", ["camel", "case"]),
            ("FRAPScase", ["frap", "case"]),
            ("SQLThing", ["sqlt", "hing"]),
            ("_Astra", ["astra"]),
            ("CAPS_CONST", ["caps", "const"]),
            ("_something_SILLY_", ["someth", "silli"]),
            ("blink182", ["blink"]),
            ("FooBar100500Bingo", ["foo", "bar", "bingo"]),
            ("Man45var", ["man", "var"]),
            ("method_name", ["method", "name"]),
            ("Method_Name", ["method", "name"]),
            ("101dalms", ["dalm"]),
            ("101_dalms", ["dalm"]),
            ("101_DalmsBug", ["dalm", "bug"]),
            ("101_Dalms45Bug7", ["dalm", "bug"]),
            ("wdSize", ["wd", "size"]),
            ("Glint", ["glint"]),
            ("foo_BAR", ["foo", "bar"]),
            ("sourced.ml.algorithms.uast_ids_to_bag",
             ["sourc", "ml", "algorithm", "uast", "ids", "to", "bag"]),
            ("WORSTnameYOUcanIMAGINE", ["worst", "name", "you", "can", "imagin"]),
            # Another bad example. Parser failed to parse it correctly
            ("SmallIdsToFoOo", ["small", "ids", "to", "fo", "oo"]),
            ("SmallIdFooo", ["small", "id", "fooo"]),
            ("ONE_M0re_.__badId.example", ["one", "m", "re", "bad", "id", "exampl"]),
            ("never_use_Such__varsableNames", ["never", "use", "such", "varsabl", "name"]),
            ("a.b.c.d", ["a", "b", "c", "d"]),
            ("A.b.Cd.E", ["a", "b", "cd", "e"]),
            ("looong_sh_loooong_sh", ["looong", "sh", "loooong", "sh"]),
            ("sh_sh_sh_sh", ["sh", "sh", "sh", "sh"]),
            ("loooong_loooong_loooong", ["loooong", "loooong", "loooong"])
        ]

        for token, correct in tokens:
            res = list(self.tp.process_token(token))
            self.assertEqual(res, correct)

        min_split_length = 3
        self.tp.min_split_length = min_split_length
        for token, correct in tokens:
            res = list(self.tp.process_token(token))
            self.assertEqual(res, [c for c in correct if len(c) >= min_split_length])

    def test_split(self):
        self.assertEqual(list(self.tp.split("set for")), ["set", "for"])
        self.assertEqual(list(self.tp.split("set /for.")), ["set", "for"])
        self.assertEqual(list(self.tp.split("NeverHav")), ["never", "hav"])
        self.assertEqual(list(self.tp.split("PrintAll")), ["print", "all"])
        self.assertEqual(list(self.tp.split("PrintAllExcept")), ["print", "all", "except"])
        self.assertEqual(
            list(self.tp.split("print really long line")),
            # 'longli' is expected artifact due to edge effects
            ["print", "really", "long", "longli"])
        self.assertEqual(
            list(self.tp.split("set /for. *&PrintAll")),
            ["set", "for", "print", "all"])
        self.assertEqual(
            list(self.tp.split("JumpDown not Here")),
            ["jump", "down", "not", "here"])

        self.assertEqual(
            list(self.tp.split("a b c d")),
            ["a", "b", "c", "d"])
        self.assertEqual(
            list(self.tp.split("a b long c d")),
            ["a", "b", "long", "blong", "longc", "d"])
        self.assertEqual(
            list(self.tp.split("AbCd")),
            ["ab", "cd"])

    def test_reconstruct(self):
        self.tp._save_token_style = True
        self.tp._single_shot = True
        self.tp.min_split_length = 1

        tokens = [
            "ONLYCAPS",
            "nocaps",
            "UpperCamelCase",
            "camelCase",
            "FRAPScase",
            "SQLThing",
            "_Astra",
            "CAPS_CONST",
            "_something_SILLY_",
            "blink182",
            "FooBar100500Bingo",
            "Man45var",
            "method_name",
            "Method_Name",
            "101dalms",
            "101_dalms",
            "101_DalmsBug",
            "101_Dalms45Bug7",
            "wdSize",
            "Glint",
            "foo_BAR",
            "sourced.ml.algorithms.uast_ids_to_bag",
            "WORSTnameYOUcanIMAGINE",
            "SmallIdsToFoOo",
            "SmallIdFooo",
            "ONE_M0re_.__badId.example",
            "never_use_Such__varsableNames",
            "a.b.c.d",
            "A.b.Cd.E",
            "looong_sh_loooong_sh",
            "sh_sh_sh_sh",
            "loooong_loooong_loooong",
        ]
        self.tp.max_token_length = max(map(len, tokens))

        for token in tokens:
            splitted_tokens = list(self.tp.split(token))
            self.assertEqual(token, self.tp.reconstruct(splitted_tokens))

    def test_split_single_shot(self):
        self.tp._single_shot = True
        self.tp.min_split_length = 1
        self.assertEqual(
            list(self.tp.split("print really long line")),
            # 'longli' is expected artifact due to edge effects
            ["print", "really", "long", "li"])
        self.assertEqual(
            list(self.tp.split("a b c d")),
            ["a", "b", "c", "d"])
        self.assertEqual(
            list(self.tp.split("a b long c d")),
            ["a", "b", "long", "c", "d"])
        self.assertEqual(
            list(self.tp.split("AbCd")),
            ["ab", "cd"])

    def test_stem(self):
        self.assertEqual(self.tp.stem("lol"), "lol")
        self.assertEqual(self.tp.stem("apple"), "appl")
        self.assertEqual(self.tp.stem("orange"), "orang")
        self.assertEqual(self.tp.stem("embedding"), "embed")
        self.assertEqual(self.tp.stem("Alfred"), "Alfred")
        self.assertEqual(self.tp.stem("Pluto"), "Pluto")

    def test_pickle(self):
        tp = pickle.loads(pickle.dumps(self.tp))
        self.assertEqual(tp.stem("embedding"), "embed")


class NoopTokenParserTests(unittest.TestCase):
    def setUp(self):
        self.tp = NoopTokenParser()

    def test_process_token(self):
        self.assertEqual(list(self.tp.process_token("abcdef")), ["abcdef"])
        self.assertEqual(list(self.tp.process_token("abcd_ef")), ["abcd_ef"])
        self.assertEqual(list(self.tp.process_token("abcDef")), ["abcDef"])


if __name__ == "__main__":
    unittest.main()
